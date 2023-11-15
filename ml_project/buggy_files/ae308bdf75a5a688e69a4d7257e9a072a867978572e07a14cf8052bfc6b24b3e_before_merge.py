def valid_id(opts, id_):
    '''
    Returns if the passed id is valid
    '''
    try:
        if any(x in id_ for x in ('/', '\\', '\0')):
            return False
        return bool(clean_path(opts['pki_dir'], id_))
    except (AttributeError, KeyError, TypeError):
        return False