    def get_func(cmd, resource_group_name, resource_name, item_name):
        client = getattr(network_client_factory(cmd.cli_ctx), resource)
        parent = getattr(client.get(resource_group_name, resource_name), prop)
        if parent is None:
            parent = []
        result = next((x for x in parent if x.name.lower() == item_name.lower()), None)
        if not result:
            raise CLIError("Item '{}' does not exist on {} '{}'".format(
                item_name, resource, resource_name))
        return result