    def concatenate_dataset(self, dataset_group, var_path):
        if 'I' in dataset_group:
            scan_size = 32
        else:
            scan_size = 16
        scans_path = 'All_Data/{dataset_group}_All/NumberOfScans'
        scans_path = scans_path.format(dataset_group=DATASET_KEYS[dataset_group])
        start_scan = 0
        data_chunks = []
        scans = self[scans_path]
        variable = self[var_path]
        # check if these are single per-granule value
        if variable.size != scans.size:
            for gscans in scans.values:
                data_chunks.append(self[var_path].isel(y=slice(start_scan, start_scan + gscans * scan_size)))
                start_scan += scan_size * 48
            return xr.concat(data_chunks, 'y')
        else:
            return self.expand_single_values(variable, scans)