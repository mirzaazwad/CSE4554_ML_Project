    def _transform(self, result, accum, values, comp_ids, transform_func,
                   is_numeric):
        comp_ids, _, ngroups = self.group_info
        if values.ndim > 3:
            # punting for now
            raise NotImplementedError("number of dimensions is currently "
                                      "limited to 3")
        elif values.ndim > 2:
            for i, chunk in enumerate(values.transpose(2, 0, 1)):

                chunk = chunk.squeeze()
                transform_func(result[:, :, i], values,
                               comp_ids, accum)
        else:
            transform_func(result, values, comp_ids, accum)

        return result