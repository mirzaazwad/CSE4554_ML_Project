    def __init__(self, values=None, column=None, dimensions=None, bins=None,
                 stat='count', source=None, **properties):
        if isinstance(stat, str):
            stat = stats[stat]()

        bin_count = properties.get('bin_count')
        if bin_count is not None and not isinstance(bin_count, list):
            properties['bin_count'] = [bin_count]
        else:
            properties['bin_count'] = []

        properties['dimensions'] = dimensions
        properties['column'] = column
        properties['bins'] = bins
        properties['stat'] = stat
        properties['values'] = values
        properties['source'] = source

        super(Bins, self).__init__(**properties)