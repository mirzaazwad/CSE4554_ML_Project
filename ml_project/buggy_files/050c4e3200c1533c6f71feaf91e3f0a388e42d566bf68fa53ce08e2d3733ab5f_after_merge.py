    def __repr__(self):
        fmt = '<{self.__class__.__name__} shape={self.shape}' \
              ' src_dtype={self.dtype!r} path={self.path!r}' \
              ' offset={self.offset}>'
        return fmt.format(self=self)