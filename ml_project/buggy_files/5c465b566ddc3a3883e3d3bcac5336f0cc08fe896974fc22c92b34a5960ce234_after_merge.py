    def __init__(self, reddit, display_name=None, _data=None):
        """Initialize a Subreddit instance.

        :param reddit: An instance of :class:`~.Reddit`.
        :param display_name: The name of the subreddit.

        .. note::

            This class should not be initialized directly. Instead obtain an instance
            via: ``reddit.subreddit("subreddit_name")``

        """
        if (display_name, _data).count(None) != 1:
            raise TypeError("Either `display_name` or `_data` must be provided.")
        if display_name:
            self.display_name = display_name
        super().__init__(reddit, _data=_data)
        self._path = API_PATH["subreddit"].format(subreddit=self)