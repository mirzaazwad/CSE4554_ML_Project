def doc(module=''):
    '''
    Return the docstrings for all modules. Optionally, specify a module or a
    function to narrow the selection.

    The strings are aggregated into a single document on the master for easy
    reading.

    CLI Example::

        salt '*' sys.doc
        salt '*' sys.doc sys
        salt '*' sys.doc sys.doc
    '''
    docs = {}
    if module:
        # allow both "sys" and "sys." to match sys, without also matching
        # sysctl
        target_mod = module + '.' if not module.endswith('.') else module
    else:
        target_mod = ''
    for fun in __salt__:
        if fun == module or fun.startswith(target_mod):
            docs[fun] = __salt__[fun].__doc__
    return docs