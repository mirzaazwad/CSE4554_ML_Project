    async def delete_pusher_by_app_id_pushkey_user_id(
        self, app_id: str, pushkey: str, user_id: str
    ) -> None:
        def delete_pusher_txn(txn, stream_id):
            self._invalidate_cache_and_stream(  # type: ignore
                txn, self.get_if_user_has_pusher, (user_id,)
            )

            self.db_pool.simple_delete_one_txn(
                txn,
                "pushers",
                {"app_id": app_id, "pushkey": pushkey, "user_name": user_id},
            )

            # it's possible for us to end up with duplicate rows for
            # (app_id, pushkey, user_id) at different stream_ids, but that
            # doesn't really matter.
            self.db_pool.simple_insert_txn(
                txn,
                table="deleted_pushers",
                values={
                    "stream_id": stream_id,
                    "app_id": app_id,
                    "pushkey": pushkey,
                    "user_id": user_id,
                },
            )

        async with self._pushers_id_gen.get_next() as stream_id:
            await self.db_pool.runInteraction(
                "delete_pusher", delete_pusher_txn, stream_id
            )