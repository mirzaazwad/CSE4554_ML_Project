def acr_webhook_list(registry_name, resource_group_name=None):
    """Lists all the webhooks for the specified container registry."
    :param str registry_name: The name of container registry
    :param str resource_group_name: The name of resource group
    """
    _, resource_group_name = managed_registry_validation(
        registry_name, resource_group_name, WEBHOOKS_NOT_SUPPORTED)
    client = get_acr_service_client(WEBHOOK_API_VERSION).webhooks

    return client.list(resource_group_name, registry_name)