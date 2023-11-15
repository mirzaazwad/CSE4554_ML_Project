    def get_measurement_columns(self, pipeline):
        '''Return the column definitions for this module's measurements'''
        columns = [
            (
                self.y_name.value,
                cellprofiler.measurement.FF_PARENT % self.x_name.value,
                cellprofiler.measurement.COLTYPE_INTEGER
            ),
            (
                self.x_name.value,
                cellprofiler.measurement.FF_CHILDREN_COUNT % self.y_name.value,
                cellprofiler.measurement.COLTYPE_INTEGER
            )
        ]

        if self.wants_per_parent_means.value:
            child_columns = self.get_child_columns(pipeline)

            columns += [
                (
                    self.x_name.value,
                    FF_MEAN % (self.y_name.value, column[1]),
                    cellprofiler.measurement.COLTYPE_FLOAT
                 ) for column in child_columns
                ]

        columns += self.get_child_measurement_columns(pipeline)

        return columns