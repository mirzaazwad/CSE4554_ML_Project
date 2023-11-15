def pcolormesh(cube, *args, **kwargs):
    """
    Draws a pseudocolor plot based on the given Cube.

    Kwargs:

    * coords: list of :class:`~iris.coords.Coord` objects or coordinate names
        Use the given coordinates as the axes for the plot. The order of the
        given coordinates indicates which axis to use for each, where the first
        element is the horizontal axis of the plot and the second element is
        the vertical axis of the plot.

    See :func:`matplotlib.pyplot.pcolormesh` for details of other valid keyword
    arguments.

    """
    result = _draw_2d_from_bounds('pcolormesh', cube, *args, **kwargs)
    return result