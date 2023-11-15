    def delete_meta(self, session_id, chunk_key):
        """
        Delete metadata from store and cache
        """
        query_key = (session_id, chunk_key)
        try:
            del self._meta_store[query_key]
        except KeyError:
            pass
        try:
            del self._meta_cache[query_key]
        except KeyError:
            pass

        # broadcast deletion into pre-determined destinations
        futures = []
        if query_key in self._meta_broadcasts:
            for dest in self._meta_broadcasts[query_key]:
                futures.append(self.ctx.actor_ref(self.default_name(), address=dest) \
                               .delete_meta(session_id, chunk_key, _wait=False, _tell=True))
        if self._kv_store_ref is not None:
            futures.append(self._kv_store_ref.delete('/sessions/%s/chunks/%s' % (session_id, chunk_key),
                                                     recursive=True, _tell=True, _wait=False))
        [f.result() for f in futures]