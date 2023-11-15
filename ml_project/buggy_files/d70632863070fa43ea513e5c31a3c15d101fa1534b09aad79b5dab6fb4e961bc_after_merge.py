            def generic(_, args, kws):
                args = (typ,) + tuple(args)
                fnty = self._get_function_type(self.context, typ)
                sig = self._get_signature(self.context, fnty, args, kws)
                sig = sig.replace(pysig=utils.pysignature(self._overload_func))
                for template in fnty.templates:
                    self._inline_overloads.update(template._inline_overloads)
                if sig is not None:
                    return sig.as_method()