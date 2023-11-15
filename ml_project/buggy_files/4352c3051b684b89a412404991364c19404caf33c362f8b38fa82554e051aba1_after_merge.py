    def reflink(self, src, dest):
        dest = shlex.quote(dest)
        src = shlex.quote(src)
        if self.uname == "Linux":
            return self.execute(f"cp --reflink {src} {dest}")

        if self.uname == "Darwin":
            return self.execute(f"cp -c {src} {dest}")

        raise DvcException(f"'{self.uname}' is not supported as a SSH remote")