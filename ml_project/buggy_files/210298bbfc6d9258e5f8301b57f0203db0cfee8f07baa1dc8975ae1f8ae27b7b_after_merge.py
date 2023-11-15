    def get_diff_input_output(self, pin, port, attrs, invert):
        self._check_feature("differential input/output", pin, attrs,
                            valid_xdrs=(0, 1, 2, 4, 7), valid_attrs=True)
        m = Module()
        i, o, t = self._get_xdr_buffer(m, pin, i_invert=invert, o_invert=invert)
        for bit in range(pin.width):
            m.submodules["{}_{}".format(pin.name, bit)] = Instance("BB",
                i_T=t,
                i_I=o[bit],
                o_O=i[bit],
                io_B=port.p[bit],
            )
        return m