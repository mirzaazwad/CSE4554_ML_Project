    async def add(self, tasks: Tuple[TTask, ...]) -> None:
        """
        add() will insert as many tasks as can be inserted until the queue fills up.
        Then it will pause until the queue is no longer full, and continue adding tasks.
        It will finally return when all tasks have been inserted.
        """
        if not isinstance(tasks, tuple):
            raise ValidationError(f"must pass a tuple of tasks to add(), but got {tasks!r}")

        already_pending = self._tasks.intersection(tasks)
        if already_pending:
            raise ValidationError(
                f"Duplicate tasks detected: {already_pending!r} are already present in the queue"
            )

        # make sure to insert the highest-priority items first, in case queue fills up
        remaining = tuple(sorted(map(self._task_wrapper, tasks)))

        while remaining:
            num_tasks = len(self._tasks)

            if self._maxsize <= 0:
                # no cap at all, immediately insert all tasks
                open_slots = len(remaining)
            elif num_tasks < self._maxsize:
                # there is room to add at least one more task
                open_slots = self._maxsize - num_tasks
            else:
                # wait until there is room in the queue
                await self._full_lock.acquire()

                # the current number of tasks has changed, restart attempt
                continue

            queueing, remaining = remaining[:open_slots], remaining[open_slots:]

            for task in queueing:
                # There will always be room in _open_queue until _maxsize is reached
                try:
                    self._open_queue.put_nowait(task)
                except asyncio.QueueFull as exc:
                    task_idx = queueing.index(task)
                    qsize = self._open_queue.qsize()
                    raise asyncio.QueueFull(
                        f'TaskQueue unsuccessful in adding task {task.original!r} ',
                        f'because qsize={qsize}, '
                        f'num_tasks={num_tasks}, maxsize={self._maxsize}, open_slots={open_slots}, '
                        f'num queueing={len(queueing)}, len(_tasks)={len(self._tasks)}, task_idx='
                        f'{task_idx}, queuing={queueing}, original msg: {exc}',
                    )

            original_queued = tuple(task.original for task in queueing)
            self._tasks.update(original_queued)

            if self._full_lock.locked() and len(self._tasks) < self._maxsize:
                self._full_lock.release()