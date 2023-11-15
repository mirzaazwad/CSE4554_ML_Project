    def __getitem__(self, key):
        """Get the attribute corresponding to the given key."""
        # Catch NotImplementedError to fix #6284 in pandas MultiIndex
        # due to NA checking not being supported on a multiindex.
        # Catch AttributeError to fix #5642 in certain special classes like xml
        # when this method is called on certain attributes.
        # Catch TypeError to prevent fatal Python crash to desktop after
        # modifying certain pandas objects ( Issue #6727 ).
        try:
            attribute_toreturn = getattr(self.__obj__, key)
        except (NotImplementedError, AttributeError, TypeError):
            attribute_toreturn = None
        return attribute_toreturn