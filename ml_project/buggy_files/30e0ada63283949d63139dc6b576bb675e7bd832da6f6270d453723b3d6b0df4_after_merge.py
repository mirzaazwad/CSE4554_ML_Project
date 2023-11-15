    def is_defined(self, objtxt, force_import=False):
        """Return True if object is defined"""
        try:
            return self.call_kernel(
                blocking=True
                ).is_defined(objtxt, force_import=force_import)
        except (TimeoutError, UnpicklingError, RuntimeError, CommError):
            return None