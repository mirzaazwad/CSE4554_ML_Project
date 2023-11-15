    def __setitem__(self, key, value):
        """Support assigning 'Dataset' objects or dictionaries of metadata.
        """
        d = value
        if hasattr(value, 'attrs'):
            # xarray.DataArray objects
            d = value.attrs
        # use value information to make a more complete DatasetID
        if not isinstance(key, DatasetID):
            if not isinstance(d, dict):
                raise ValueError("Key must be a DatasetID when value is not an xarray DataArray or dict")
            old_key = key
            key = self.get_key(key)
            if key is None:
                if isinstance(old_key, (str, six.text_type)):
                    new_name = old_key
                else:
                    new_name = d.get("name")
                # this is a new key and it's not a full DatasetID tuple
                key = DatasetID(name=new_name,
                                resolution=d.get("resolution"),
                                wavelength=d.get("wavelength"),
                                polarization=d.get("polarization"),
                                calibration=d.get("calibration"),
                                modifiers=d.get("modifiers", tuple()))
                if key.name is None and key.wavelength is None:
                    raise ValueError(
                        "One of 'name' or 'wavelength' attrs values should be set.")

        # update the 'value' with the information contained in the key
        if isinstance(d, dict):
            d["name"] = key.name
            # XXX: What should users be allowed to modify?
            d["resolution"] = key.resolution
            d["calibration"] = key.calibration
            d["polarization"] = key.polarization
            d["modifiers"] = key.modifiers
            # you can't change the wavelength of a dataset, that doesn't make
            # sense
            if "wavelength" in d and d["wavelength"] != key.wavelength:
                raise TypeError("Can't change the wavelength of a dataset")

        return super(DatasetDict, self).__setitem__(key, value)