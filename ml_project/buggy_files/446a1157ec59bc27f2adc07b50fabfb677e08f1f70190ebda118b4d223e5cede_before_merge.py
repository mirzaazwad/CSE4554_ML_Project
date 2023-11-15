    def register(self, category, key, value):
        if category not in KNOWN_CATEGORIES:
            raise TuneError("Unknown category {} not among {}".format(
                category, KNOWN_CATEGORIES))
        self._all_objects[(category, key)] = value