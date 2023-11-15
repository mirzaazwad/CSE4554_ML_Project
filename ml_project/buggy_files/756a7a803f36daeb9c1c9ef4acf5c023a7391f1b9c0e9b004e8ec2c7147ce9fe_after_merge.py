def generate_admin_dict(array):
    admin_info = {}
    api_version = array._list_available_rest_versions()
    if ADMIN_API_VERSION in api_version:
        admins = array.list_admins()
        for admin in range(0, len(admins)):
            admin_name = admins[admin]['name']
            admin_info[admin_name] = {
                'type': admins[admin]['type'],
                'role': admins[admin]['role'],
            }
    return admin_info