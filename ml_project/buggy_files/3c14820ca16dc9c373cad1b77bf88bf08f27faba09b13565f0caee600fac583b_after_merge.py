    def extract_hierarchy(self, classification):
        """Given a classification, return a list of parts in the hierarchy."""
        return hierarchy_utils.parse_escaped_hierarchical_category_name(classification)