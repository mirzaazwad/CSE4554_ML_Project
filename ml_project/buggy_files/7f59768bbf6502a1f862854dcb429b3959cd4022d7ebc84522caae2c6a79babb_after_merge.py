def any(a, axis=None, out=None, keepdims=None, combine_size=None):
    """
    Test whether any tensor element along a given axis evaluates to True.

    Returns single boolean unless `axis` is not ``None``

    Parameters
    ----------
    a : array_like
        Input tensor or object that can be converted to an array.
    axis : None or int or tuple of ints, optional
        Axis or axes along which a logical OR reduction is performed.
        The default (`axis` = `None`) is to perform a logical OR over all
        the dimensions of the input array. `axis` may be negative, in
        which case it counts from the last to the first axis.

        If this is a tuple of ints, a reduction is performed on multiple
        axes, instead of a single axis or all the axes as before.
    out : Tensor, optional
        Alternate output tensor in which to place the result.  It must have
        the same shape as the expected output and its type is preserved
        (e.g., if it is of type float, then it will remain so, returning
        1.0 for True and 0.0 for False, regardless of the type of `a`).
        See `doc.ufuncs` (Section "Output arguments") for details.

    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the input tensor.

        If the default value is passed, then `keepdims` will not be
        passed through to the `any` method of sub-classes of
        `Tensor`, however any non-default value will be.  If the
        sub-classes `sum` method does not implement `keepdims` any
        exceptions will be raised.
    combine_size: int, optional
        The number of chunks to combine.

    Returns
    -------
    any : bool or Tensor
        A new boolean or `Tensor` is returned unless `out` is specified,
        in which case a reference to `out` is returned.

    See Also
    --------
    Tensor.any : equivalent method

    all : Test whether all elements along a given axis evaluate to True.

    Notes
    -----
    Not a Number (NaN), positive infinity and negative infinity evaluate
    to `True` because these are not equal to zero.

    Examples
    --------
    >>> import mars.tensor as mt

    >>> mt.any([[True, False], [True, True]]).execute()
    True

    >>> mt.any([[True, False], [False, False]], axis=0).execute()
    array([ True, False])

    >>> mt.any([-1, 0, 5]).execute()
    True

    >>> mt.any(mt.nan).execute()
    True

    """
    a = astensor(a)
    if a.dtype == np.object_:
        dtype = a.dtype
    else:
        dtype = np.dtype(bool)
    op = TensorAny(axis=axis, dtype=dtype, keepdims=keepdims, combine_size=combine_size)
    return op(a, out=out)