def _get_name_map(saltenv='base'):
    '''
    Return a reverse map of full pkg names to the names recognized by winrepo.
    '''
    u_name_map = {}
    name_map = get_repo_data(saltenv).get('name_map', {})

    if not six.PY2:
        return name_map

    for k in name_map:
        u_name_map[k.decode('utf-8')] = name_map[k]
    return u_name_map