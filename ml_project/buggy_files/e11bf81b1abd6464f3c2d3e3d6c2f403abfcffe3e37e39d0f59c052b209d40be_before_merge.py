    def images(self, **kwargs):
        """
        Get the images (posters) that we have stored for a TV season by season
        number.

        Args:
            language: (optional) ISO 639 code.
            include_image_language: (optional) Comma separated, a valid
                                    ISO 69-1.

        Returns:
            A dict respresentation of the JSON returned from the API.
        """
        path = self._get_id_season_number_path('images')

        response = self._GET(path, kwargs)
        self._set_attrs_to_values(response)
        return response