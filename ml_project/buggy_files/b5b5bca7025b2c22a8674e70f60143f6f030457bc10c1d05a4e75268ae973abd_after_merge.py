    def __init__(self, filename):
        """Init the format reader."""
        self.types, self.stypes, self.scales = parse_format(filename)

        self.translator = {}

        for key, val in self.types.items():
            self.translator[val] = (self.scales[key], self.stypes[key])