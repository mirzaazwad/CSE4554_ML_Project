    def set_params(self, **kwargs):
        """
        Take in a dictionary of parameters and applies attack-specific checks before saving them as attributes.

        :param theta: Perturbation introduced to each modified feature per step (can be positive or negative)
        :type theta: `float`
        :param gamma: Maximum percentage of perturbed features (between 0 and 1)
        :type gamma: `float`
        """
        # Save attack-specific parameters
        super(SaliencyMapMethod, self).set_params(**kwargs)

        if self.gamma <= 0 or self.gamma > 1:
            raise ValueError("The total perturbation percentage `gamma` must be between 0 and 1.")

        return True