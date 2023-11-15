    def set_python_info(self, python_executable):
        cmd = [str(python_executable), VERSION_QUERY_SCRIPT]
        result = subprocess.check_output(cmd, universal_newlines=True)
        answer = json.loads(result)
        answer["executable"] = python_executable
        self.dict["python"] = answer