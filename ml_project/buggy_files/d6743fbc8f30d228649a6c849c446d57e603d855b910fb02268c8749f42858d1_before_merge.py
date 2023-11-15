    def __init__(self, *args, **kwargs):

        self.plugin_name = self.__module__.split('.')[-1]
        self._timeout = float(C.CACHE_PLUGIN_TIMEOUT)
        self._cache = {}
        self._cache_dir = None

        if C.CACHE_PLUGIN_CONNECTION:
            # expects a dir path
            self._cache_dir = os.path.expanduser(os.path.expandvars(C.CACHE_PLUGIN_CONNECTION))

        if not self._cache_dir:
            raise AnsibleError("error, '%s' cache plugin requires the 'fact_caching_connection' config option"
                    " to be set (to a writeable directory path)" % self.plugin_name)

        if not os.path.exists(self._cache_dir):
            try:
                os.makedirs(self._cache_dir)
            except (OSError,IOError) as e:
                display.warning("error in '%s' cache plugin while trying to create cache dir %s : %s" % (self.plugin_name, self._cache_dir, to_bytes(e)))
                return None