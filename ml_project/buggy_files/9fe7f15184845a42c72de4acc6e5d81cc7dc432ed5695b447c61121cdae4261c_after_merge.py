    async def tracks_in_folder(self):
        tracks = []
        async for track in self.multiglob(*[f"{ext}" for ext in self._all_music_ext]):
            with contextlib.suppress(ValueError):
                if track.path.parent != self.localtrack_folder and track.path.relative_to(
                    self.path
                ):
                    tracks.append(Query.process_input(track, self._localtrack_folder))
        return sorted(tracks, key=lambda x: x.to_string_user().lower())