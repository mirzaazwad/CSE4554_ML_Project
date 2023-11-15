    def new_module(self):
        ''' Make a fresh module to run in.

        Returns:
            Module

        '''
        if self.failed:
            return None

        module_name = 'bk_script_' + make_id().replace('-', '')
        module = ModuleType(str(module_name)) # str needed for py2.7
        module.__dict__['__file__'] = os.path.abspath(self._path)

        return module