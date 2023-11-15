    def from_json(cls, dataset_class, tag, vr, value, value_key,
                  bulk_data_uri_handler=None, encodings=None):
        """Return a :class:`DataElement` from JSON.

        Parameters
        ----------
        dataset_class : Dataset derived class
            Class used to create sequence items.
        tag : BaseTag
            The data element tag.
        vr : str
            The data element value representation.
        value : list
            The data element's value(s).
        value_key : str or None
            Key of the data element that contains the value
            (options: ``{"Value", "InlineBinary", "BulkDataURI"}``)
        bulk_data_uri_handler: callable or None
            Callable function that accepts the "BulkDataURI" of the JSON
            representation of a data element and returns the actual value of
            that data element (retrieved via DICOMweb WADO-RS)

        Returns
        -------
        DataElement
        """
        # TODO: test wado-rs retrieve wrapper
        try:
            vm = dictionary_VM(tag)
        except KeyError:
            # Private tag
            vm = str(len(value))
        if value_key == 'Value':
            if not(isinstance(value, list)):
                fmt = '"{}" of data element "{}" must be a list.'
                raise TypeError(fmt.format(value_key, tag))
        elif value_key in {'InlineBinary', 'BulkDataURI'}:
            if isinstance(value, list):
                fmt = '"{}" of data element "{}" must be a {}.'
                expected_type = ('string' if value_key == 'BulkDataURI'
                                 else 'bytes-like object')
                raise TypeError(fmt.format(value_key, tag, expected_type))
        if vr == 'SQ':
            elem_value = []
            for value_item in value:
                ds = dataset_class()
                if value_item:
                    for key, val in value_item.items():
                        if 'vr' not in val:
                            fmt = 'Data element "{}" must have key "vr".'
                            raise KeyError(fmt.format(tag))
                        unique_value_keys = tuple(
                            set(val.keys()) & set(jsonrep.JSON_VALUE_KEYS)
                        )
                        if len(unique_value_keys) == 0:
                            logger.debug(
                                'data element has neither key "{}".'.format(
                                    '" nor "'.join(jsonrep.JSON_VALUE_KEYS)
                                )
                            )
                            elem = DataElement(tag=tag, value='', VR=vr)
                        else:
                            value_key = unique_value_keys[0]
                            elem = cls.from_json(
                                dataset_class, key, val['vr'],
                                val[value_key], value_key
                            )
                        ds.add(elem)
                elem_value.append(ds)
        elif vr == 'PN':
            # Special case, see DICOM Part 18 Annex F2.2
            elem_value = []
            for v in value:
                if not isinstance(v, dict):
                    # Some DICOMweb services get this wrong, so we
                    # workaround the issue and warn the user
                    # rather than raising an error.
                    logger.error(
                        'value of data element "{}" with VR Person Name (PN) '
                        'is not formatted correctly'.format(tag)
                    )
                    elem_value.append(v)
                else:
                    elem_value.extend(list(v.values()))
            if vm == '1':
                try:
                    elem_value = elem_value[0]
                except IndexError:
                    elem_value = ''
        else:
            if vm == '1':
                if value_key == 'InlineBinary':
                    elem_value = base64.b64decode(value)
                elif value_key == 'BulkDataURI':
                    if bulk_data_uri_handler is None:
                        logger.warning(
                            'no bulk data URI handler provided for retrieval '
                            'of value of data element "{}"'.format(tag)
                        )
                        elem_value = b''
                    else:
                        elem_value = bulk_data_uri_handler(value)
                else:
                    if value:
                        elem_value = value[0]
                    else:
                        elem_value = value
            else:
                elem_value = value
        if elem_value is None:
            logger.warning('missing value for data element "{}"'.format(tag))
            elem_value = ''

        elem_value = jsonrep.convert_to_python_number(elem_value, vr)

        try:
            if compat.in_py2 and vr == "PN":
                elem_value = PersonNameUnicode(elem_value, 'UTF8')
            return DataElement(tag=tag, value=elem_value, VR=vr)
        except Exception:
            raise ValueError(
                'Data element "{}" could not be loaded from JSON: {}'.format(
                    tag, elem_value
                    )
            )