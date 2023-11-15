    def _get_sensor_names(self):
        """Join the sensors from all loaded readers."""
        # if the user didn't tell us what sensors to work with, let's figure it
        # out
        if not self.info.get('sensor'):
            # reader finder could return multiple readers
            return set([sensor for reader_instance in self.readers.values()
                        for sensor in reader_instance.sensor_names])
        elif not isinstance(self.info['sensor'], (set, tuple, list)):
            return set([self.info['sensor']])
        else:
            return set(self.info['sensor'])