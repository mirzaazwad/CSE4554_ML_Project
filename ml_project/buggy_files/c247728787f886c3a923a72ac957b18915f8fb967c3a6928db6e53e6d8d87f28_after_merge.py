    def __init__(self, filename, filename_info, filetype_info, cal,
                 engine=None):
        """Init the file handler."""
        super(NCOLCI1B, self).__init__(filename, filename_info,
                                       filetype_info)
        self.cal = cal.nc