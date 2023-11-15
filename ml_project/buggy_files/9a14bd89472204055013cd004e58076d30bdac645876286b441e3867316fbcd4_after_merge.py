    def remote_input_newer_than_local(self):
        files = set()
        for f in self.remote_input:
            if (f.exists_remote and f.exists_local) and (
                f.mtime.remote() > f.mtime.local(follow_symlinks=True)
            ):
                files.add(f)
        return files