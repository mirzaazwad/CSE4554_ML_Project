        def wrapper(*args, **kwargs):
            with context.func_globals_inject(f, **inject_globals):
                return f(*args, **kwargs)