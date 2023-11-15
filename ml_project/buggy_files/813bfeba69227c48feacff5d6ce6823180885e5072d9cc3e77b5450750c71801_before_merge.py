def unicode_gt(a, b):
    if isinstance(a, types.UnicodeType) and isinstance(b, types.UnicodeType):
        def gt_impl(a, b):
            minlen = min(len(a), len(b))
            eqcode = _cmp_region(a, 0, b, 0, minlen)
            if eqcode == 1:
                return True
            elif eqcode == 0:
                return len(a) > len(b)
            return False
        return gt_impl