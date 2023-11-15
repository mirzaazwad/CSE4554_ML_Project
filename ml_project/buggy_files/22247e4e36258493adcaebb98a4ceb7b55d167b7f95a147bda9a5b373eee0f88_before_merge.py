    def fillna(self, value=None, method='pad', inplace=False):
        dense = self.to_dense()
        filled = dense.fillna(value=value, method=method)
        result = filled.to_sparse(kind=self.kind,
                                  fill_value=self.fill_value)

        if inplace:
            self.sp_values[:] = result.values
            return self
        else:
            return result