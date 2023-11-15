    def check_range(self, j):
        """Check that j is a valid index into self."""
        if j < 0 or j >= self.size:
            raise QISKitIndexError("register index out of range")