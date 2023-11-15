def make_mask(m, copy=False, shrink=True, dtype=MaskType):
    """
    Create a boolean mask from an array.

    Return `m` as a boolean mask, creating a copy if necessary or requested.
    The function can accept any sequence that is convertible to integers,
    or ``nomask``.  Does not require that contents must be 0s and 1s, values
    of 0 are interepreted as False, everything else as True.

    Parameters
    ----------
    m : array_like
        Potential mask.
    copy : bool, optional
        Whether to return a copy of `m` (True) or `m` itself (False).
    shrink : bool, optional
        Whether to shrink `m` to ``nomask`` if all its values are False.
    dtype : dtype, optional
        Data-type of the output mask. By default, the output mask has a
        dtype of MaskType (bool). If the dtype is flexible, each field has
        a boolean dtype. This is ignored when `m` is ``nomask``, in which
        case ``nomask`` is always returned.

    Returns
    -------
    result : ndarray
        A boolean mask derived from `m`.

    Examples
    --------
    >>> import numpy.ma as ma
    >>> m = [True, False, True, True]
    >>> ma.make_mask(m)
    array([ True, False,  True,  True], dtype=bool)
    >>> m = [1, 0, 1, 1]
    >>> ma.make_mask(m)
    array([ True, False,  True,  True], dtype=bool)
    >>> m = [1, 0, 2, -3]
    >>> ma.make_mask(m)
    array([ True, False,  True,  True], dtype=bool)

    Effect of the `shrink` parameter.

    >>> m = np.zeros(4)
    >>> m
    array([ 0.,  0.,  0.,  0.])
    >>> ma.make_mask(m)
    False
    >>> ma.make_mask(m, shrink=False)
    array([False, False, False, False], dtype=bool)

    Using a flexible `dtype`.

    >>> m = [1, 0, 1, 1]
    >>> n = [0, 1, 0, 0]
    >>> arr = []
    >>> for man, mouse in zip(m, n):
    ...     arr.append((man, mouse))
    >>> arr
    [(1, 0), (0, 1), (1, 0), (1, 0)]
    >>> dtype = np.dtype({'names':['man', 'mouse'],
                          'formats':[int, int]})
    >>> arr = np.array(arr, dtype=dtype)
    >>> arr
    array([(1, 0), (0, 1), (1, 0), (1, 0)],
          dtype=[('man', '<i4'), ('mouse', '<i4')])
    >>> ma.make_mask(arr, dtype=dtype)
    array([(True, False), (False, True), (True, False), (True, False)],
          dtype=[('man', '|b1'), ('mouse', '|b1')])

    """
    if m is nomask:
        return nomask

    # Make sure the input dtype is valid.
    dtype = make_mask_descr(dtype)
    
    # legacy boolean special case: "existence of fields implies true"
    if isinstance(m, ndarray) and m.dtype.fields and dtype == np.bool_:
        return np.ones(m.shape, dtype=dtype)

    # Fill the mask in case there are missing data; turn it into an ndarray.
    result = np.array(filled(m, True), copy=copy, dtype=dtype, subok=True)
    # Bas les masques !
    if shrink and (not result.dtype.names) and (not result.any()):
        return nomask
    else:
        return result