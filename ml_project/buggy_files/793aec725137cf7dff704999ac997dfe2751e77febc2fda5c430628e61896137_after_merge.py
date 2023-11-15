    def display(self, workspace, figure):
        if not self.show_window:
            return

        dimensions = workspace.display_data.dimensions

        figure.set_subplots((2, 2), dimensions=dimensions)

        child_labels = workspace.display_data.child_labels

        parents_of = workspace.display_data.parents_of

        parent_labels = workspace.display_data.parent_labels

        #
        # discover the mapping so that we can apply it to the children
        #
        mapping = numpy.arange(workspace.display_data.parent_count + 1)

        mapping[parent_labels] = parent_labels

        parent_labeled_children = numpy.zeros(child_labels.shape, int)

        mask = child_labels > 0

        parent_labeled_children[mask] = mapping[parents_of[child_labels[mask] - 1]]

        figure.subplot_imshow_labels(
            0,
            0,
            parent_labels,
            title=self.x_name.value,
            dimensions=dimensions

        )

        figure.subplot_imshow_labels(
            1,
            0,
            child_labels,
            title=self.y_name.value,
            dimensions=dimensions
        )

        figure.subplot_imshow_labels(
            0,
            1,
            parent_labeled_children,
            "{} labeled by {}".format(self.y_name.value, self.x_name.value),
            dimensions=dimensions
        )