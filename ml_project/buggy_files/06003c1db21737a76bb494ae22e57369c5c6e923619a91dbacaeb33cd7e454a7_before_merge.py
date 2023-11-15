    def _pyversion(self):
        include_dir = vistir.compat.Path(self.virtualenv_location) / "include"
        python_path = next((x for x in include_dir.iterdir() if x.name.startswith("python")), None)
        if python_path:
            python_version = python_path.name.replace("python", "")
            py_version_short, abiflags = python_version[:3], python_version[3:]
            return {"py_version_short": py_version_short, "abiflags": abiflags}
        return {}