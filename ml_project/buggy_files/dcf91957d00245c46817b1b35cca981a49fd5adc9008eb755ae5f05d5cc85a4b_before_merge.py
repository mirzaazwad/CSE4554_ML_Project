    def detect_poison(self, **kwargs):
        """
        Returns poison detected.

        :param kwargs: a dictionary of detection-specific parameters
        :type kwargs: `dict`
        :return: 1) confidence_level, 2) is_clean_lst : type List[int], where is_clean_lst[i]=1 means that x_train[i]
                there is clean and is_clean_lst[i]=0, means that x_train[i] was classified as poison
        :rtype: `tuple`
        """
        self.set_params(**kwargs)

        if not self.activations_by_class:
            activations = self._get_activations()
            self.activations_by_class = self._segment_by_class(activations, self.y_train)
        self.clusters_by_class, self.red_activations_by_class = self.cluster_activations()
        self.assigned_clean_by_class = self.analyze_clusters()
        # Here, assigned_clean_by_class[i][j] is 1 if the jth datapoint in the ith class was
        # determined to be clean by activation cluster

        # Build an array that matches the original indexes of x_train
        n_train = len(self.x_train)
        indices_by_class = self._segment_by_class(np.arange(n_train), self.y_train)
        self.is_clean_lst = [0] * n_train
        self.confidence_level = [1] * n_train
        for assigned_clean, dp in zip(self.assigned_clean_by_class, indices_by_class):
            for assignment, index_dp in zip(assigned_clean, dp):
                if assignment == 1:
                    self.is_clean_lst[index_dp] = 1

        return self.confidence_level, self.is_clean_lst