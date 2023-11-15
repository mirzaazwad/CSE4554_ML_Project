    def object_locate(self, account, container, obj,
                      version=None, properties=True, **kwargs):
        """
        Get a description of the object along with the list of its chunks.

        :param account: name of the account in which the object is stored
        :param container: name of the container in which the object is stored
        :param obj: name of the object to query
        :param version: version of the object to query
        :param properties: should the request return object properties
            along with content description
        :type properties: `bool`

        :returns: a tuple with object metadata `dict` as first element
            and chunk `list` as second element
        """
        obj_meta, chunks = self.container.content_locate(
            account, container, obj, version=version,
            properties=properties, **kwargs)
        return obj_meta, chunks