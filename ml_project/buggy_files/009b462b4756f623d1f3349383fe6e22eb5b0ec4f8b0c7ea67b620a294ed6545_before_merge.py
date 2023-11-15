    def _prepare_inter_op(self, other):
        """
        Implement [METHOD_NAME].

        TODO: Add more details for this docstring template.

        Parameters
        ----------
        What arguments does this function have.
        [
        PARAMETER_NAME: PARAMETERS TYPES
            Description.
        ]

        Returns
        -------
        What this returns (if anything)
        """
        if isinstance(other, Series):
            new_self = self.copy()
            new_self.name = "__reduced__"
            new_other = other.copy()
            new_other.name = "__reduced__"
        else:
            new_self = self
            new_other = other
        return new_self, new_other