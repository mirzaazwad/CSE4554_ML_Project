    def set_data(self, data):
        """Set table data"""
        if data is not None:
            self.source_model.set_data(data, self.dictfilter)
            self.source_model.reset()
            self.sortByColumn(0, Qt.AscendingOrder)