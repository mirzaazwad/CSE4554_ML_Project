    def _store_object(self, obj):
        self._wr = _PickleableWeakRef(obj)