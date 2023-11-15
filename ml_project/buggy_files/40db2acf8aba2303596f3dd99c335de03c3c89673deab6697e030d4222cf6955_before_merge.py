    def get_diff_output(self, pin, p_port, n_port, attrs, invert):
        self._check_feature("differential output", pin, attrs,
                            valid_xdrs=(0, 1, 2, 4, 7), valid_attrs=True)
        m = Module()
        i, o, t = self._get_xdr_buffer(m, pin, o_invert=invert)
        for bit in range(len(p_port)):
            m.submodules["{}_{}".format(pin.name, bit)] = Instance("OB",
                i_I=o[bit],
                o_O=p_port[bit],
            )
        return m