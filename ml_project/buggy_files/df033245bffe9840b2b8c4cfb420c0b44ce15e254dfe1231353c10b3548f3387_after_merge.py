def _affinity_method(op, left, *args, **kwargs):
    # type: (str, GeometryArray, ...) -> GeometryArray

    # not all shapely.affinity methods can handle empty geometries:
    # affine_transform itself works (as well as translate), but rotate, scale
    # and skew fail (they try to unpack the bounds).
    # Here: consistently returning empty geom for input empty geom
    out = []
    for geom in left.data:
        if geom is None or geom.is_empty:
            res = geom
        else:
            res = getattr(shapely.affinity, op)(geom, *args, **kwargs)
        out.append(res)
    data = np.empty(len(left), dtype=object)
    data[:] = out
    return GeometryArray(data)