    def _get_unitary_matrix(self, unitary):
        """Return the matrix representing a unitary operation.

        Args:
            unitary (~.Operation): a PennyLane unitary operation

        Returns:
            array[complex]: Returns a 2D matrix representation of
            the unitary in the computational basis, or, in the case of a diagonal unitary,
            a 1D array representing the matrix diagonal.
        """
        op_name = unitary.name
        if op_name in self.parametric_ops:
            if op_name == "MultiRZ":
                return self.parametric_ops[unitary.name](*unitary.parameters, len(unitary.wires))
            return self.parametric_ops[unitary.name](*unitary.parameters)

        if isinstance(unitary, DiagonalOperation):
            return unitary.eigvals

        return unitary.matrix