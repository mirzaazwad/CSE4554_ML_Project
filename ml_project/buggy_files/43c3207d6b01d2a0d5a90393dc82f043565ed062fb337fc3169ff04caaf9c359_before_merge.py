    def _strategy_htex_auto_scale(self, tasks, *args, kind=None, **kwargs):
        """ HTEX specific auto scaling strategy

        This strategy works only for HTEX. This strategy will scale up by
        requesting additional compute resources via the provider when the
        workload requirements exceed the provisioned capacity. The scale out
        behavior is exactly like the 'simple' strategy.

        If there are idle blocks during execution, this strategy will terminate
        those idle blocks specifically. When # of tasks >> # of blocks, HTEX places
        tasks evenly across blocks, which makes it rather difficult to ensure that
        some blocks will reach 0% utilization. Consequently, this strategy can be
        expected to scale down effectively only when # of workers, or tasks executing
        per block is close to 1.

        Args:
            - tasks (task_ids): Not used here.

        KWargs:
            - kind (Not used)
        """

        for label, executor in self.dfk.executors.items():
            if not executor.scaling_enabled:
                continue

            # Tasks that are either pending completion
            active_tasks = executor.outstanding

            status = executor.status()
            self.unset_logging()

            # FIXME we need to handle case where provider does not define these
            # FIXME probably more of this logic should be moved to the provider
            min_blocks = executor.provider.min_blocks
            max_blocks = executor.provider.max_blocks
            if isinstance(executor, HighThroughputExecutor):

                tasks_per_node = executor.workers_per_node
            elif isinstance(executor, ExtremeScaleExecutor):
                tasks_per_node = executor.ranks_per_node

            nodes_per_block = executor.provider.nodes_per_block
            parallelism = executor.provider.parallelism

            running = sum([1 for x in status.values() if x.state == JobState.RUNNING])
            pending = sum([1 for x in status.values() if x.state == JobState.PENDING])
            active_blocks = running + pending
            active_slots = active_blocks * tasks_per_node * nodes_per_block

            if hasattr(executor, 'connected_workers'):
                logger.debug('Executor {} has {} active tasks, {}/{} running/pending blocks, and {} connected workers'.format(
                    label, active_tasks, running, pending, executor.connected_workers))
            else:
                logger.debug('Executor {} has {} active tasks and {}/{} running/pending blocks'.format(
                    label, active_tasks, running, pending))

            # reset kill timer if executor has active tasks
            if active_tasks > 0 and self.executors[executor.label]['idle_since']:
                self.executors[executor.label]['idle_since'] = None

            # Case 1
            # No tasks.
            if active_tasks == 0:
                # Case 1a
                # Fewer blocks that min_blocks
                if active_blocks <= min_blocks:
                    # Ignore
                    # logger.debug("Strategy: Case.1a")
                    pass

                # Case 1b
                # More blocks than min_blocks. Scale down
                else:
                    # We want to make sure that max_idletime is reached
                    # before killing off resources
                    if not self.executors[executor.label]['idle_since']:
                        logger.debug("Executor {} has 0 active tasks; starting kill timer (if idle time exceeds {}s, resources will be removed)".format(
                            label, self.max_idletime)
                        )
                        self.executors[executor.label]['idle_since'] = time.time()

                    idle_since = self.executors[executor.label]['idle_since']
                    if (time.time() - idle_since) > self.max_idletime:
                        # We have resources idle for the max duration,
                        # we have to scale_in now.
                        logger.debug("Idle time has reached {}s for executor {}; removing resources".format(
                            self.max_idletime, label)
                        )
                        executor.scale_in(active_blocks - min_blocks)

                    else:
                        pass
                        # logger.debug("Strategy: Case.1b. Waiting for timer : {0}".format(idle_since))

            # Case 2
            # More tasks than the available slots.
            elif (float(active_slots) / active_tasks) < parallelism:
                # Case 2a
                # We have the max blocks possible
                if active_blocks >= max_blocks:
                    # Ignore since we already have the max nodes
                    # logger.debug("Strategy: Case.2a")
                    pass

                # Case 2b
                else:
                    # logger.debug("Strategy: Case.2b")
                    excess = math.ceil((active_tasks * parallelism) - active_slots)
                    excess_blocks = math.ceil(float(excess) / (tasks_per_node * nodes_per_block))
                    excess_blocks = min(excess_blocks, max_blocks - active_blocks)
                    logger.debug("Requesting {} more blocks".format(excess_blocks))
                    executor.scale_out(excess_blocks)

            elif active_slots == 0 and active_tasks > 0:
                # Case 4
                logger.debug("Requesting single slot")
                if active_blocks < max_blocks:
                    executor.scale_out(1)

            # Case 4
            # More slots than tasks
            elif active_slots > 0 and active_slots > active_tasks:
                logger.debug("More slots than tasks")
                if isinstance(executor, HighThroughputExecutor):
                    if active_blocks > min_blocks:
                        executor.scale_in(1, force=False, max_idletime=self.max_idletime)
            # Case 3
            # tasks ~ slots
            else:
                # logger.debug("Strategy: Case 3")
                pass