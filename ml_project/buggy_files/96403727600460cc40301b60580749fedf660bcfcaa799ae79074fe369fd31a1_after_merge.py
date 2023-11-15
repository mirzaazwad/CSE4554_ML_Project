    def __call__(self, datasets, **info):
        refl_data, sensor_aa, sensor_za, solar_aa, solar_za = datasets
        if refl_data.attrs.get("rayleigh_corrected"):
            return refl_data

        if os.path.isfile(self.dem_file):
            LOG.debug("Loading CREFL averaged elevation information from: %s",
                      self.dem_file)
            from netCDF4 import Dataset as NCDataset
            # HDF4 file, NetCDF library needs to be compiled with HDF4 support
            nc = NCDataset(self.dem_file, "r")
            avg_elevation = nc.variables[self.dem_sds][:]
        else:
            avg_elevation = None

        from satpy.composites.crefl_utils import run_crefl, get_coefficients

        percent = refl_data.attrs["units"] == "%"

        coefficients = get_coefficients(refl_data.attrs["sensor"],
                                        refl_data.attrs["wavelength"],
                                        refl_data.attrs["resolution"])

        results = run_crefl(refl_data,
                            coefficients,
                            sensor_aa.attrs["area"].lons,
                            sensor_aa.attrs["area"].lats,
                            sensor_aa,
                            sensor_za,
                            solar_aa,
                            solar_za,
                            avg_elevation=avg_elevation,
                            percent=percent, )

        info.update(refl_data.attrs)
        info["rayleigh_corrected"] = True
        factor = 100. if percent else 1.
        proj = Dataset(data=results.data * factor,
                       mask=results.mask,
                       dtype=results.dtype,
                       **info)

        self.apply_modifier_info(refl_data, proj)

        return proj