def tag(name):
    """Decorator to define a tag macro called `name`.
    """
    def _(fn):
        _name = mangle('#{}'.format(name))

        if not PY3:
            _name = _name.encode('UTF-8')

        fn = rename_function(fn, _name)

        module = inspect.getmodule(fn)

        module_name = module.__name__
        if module_name.startswith("hy.core"):
            module_name = None

        module_tags = module.__dict__.setdefault('__tags__', {})
        module_tags[mangle(name)] = fn

        return fn
    return _