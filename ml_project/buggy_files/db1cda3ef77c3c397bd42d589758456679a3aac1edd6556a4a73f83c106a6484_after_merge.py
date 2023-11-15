def pl_multi_process(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        queue = Queue()
        proc = Process(target=inner_f, args=(queue, func, *args), kwargs=kwargs)
        proc.start()
        proc.join(10)
        try:
            return queue.get_nowait()
        except q.Empty:
            return False

    return wrapper