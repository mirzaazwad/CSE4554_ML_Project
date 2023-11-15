def isentropic_interpolation(theta_levels, pressure, temperature, *args, **kwargs):
    r"""Interpolate data in isobaric coordinates to isentropic coordinates.

    Parameters
    ----------
    theta_levels : array
        One-dimensional array of desired theta surfaces
    pressure : array
        One-dimensional array of pressure levels
    temperature : array
        Array of temperature
    args : array, optional
        Any additional variables will be interpolated to each isentropic level.

    Returns
    -------
    list
        List with pressure at each isentropic level, followed by each additional
        argument interpolated to isentropic coordinates.

    Other Parameters
    ----------------
    axis : int, optional
        The axis corresponding to the vertical in the temperature array, defaults to 0.
    tmpk_out : bool, optional
        If true, will calculate temperature and output as the last item in the output list.
        Defaults to False.
    max_iters : int, optional
        The maximum number of iterations to use in calculation, defaults to 50.
    eps : float, optional
        The desired absolute error in the calculated value, defaults to 1e-6.

    Notes
    -----
    Input variable arrays must have the same number of vertical levels as the pressure levels
    array. Pressure is calculated on isentropic surfaces by assuming that temperature varies
    linearly with the natural log of pressure. Linear interpolation is then used in the
    vertical to find the pressure at each isentropic level. Interpolation method from
    [Ziv1994]_. Any additional arguments are assumed to vary linearly with temperature and will
    be linearly interpolated to the new isentropic levels.

    See Also
    --------
    potential_temperature

    """
    # iteration function to be used later
    # Calculates theta from linearly interpolated temperature and solves for pressure
    def _isen_iter(iter_log_p, isentlevs_nd, ka, a, b, pok):
        exner = pok * np.exp(-ka * iter_log_p)
        t = a * iter_log_p + b
        # Newton-Raphson iteration
        f = isentlevs_nd - t * exner
        fp = exner * (ka * t - a)
        return iter_log_p - (f / fp)

    # Change when Python 2.7 no longer supported
    # Pull out keyword arguments
    tmpk_out = kwargs.pop('tmpk_out', False)
    max_iters = kwargs.pop('max_iters', 50)
    eps = kwargs.pop('eps', 1e-6)
    axis = kwargs.pop('axis', 0)

    # Get dimensions in temperature
    ndim = temperature.ndim

    # Convert units
    pres = pressure.to('hPa')
    temperature = temperature.to('kelvin')

    slices = [np.newaxis] * ndim
    slices[axis] = slice(None)
    pres = pres[slices]
    pres = np.broadcast_to(pres, temperature.shape) * pres.units

    # Sort input data
    sort_pres = np.argsort(pres.m, axis=axis)
    sort_pres = np.swapaxes(np.swapaxes(sort_pres, 0, axis)[::-1], 0, axis)
    sorter = broadcast_indices(pres, sort_pres, ndim, axis)
    levs = pres[sorter]
    theta_levels = np.asanyarray(theta_levels.to('kelvin')).reshape(-1)
    sort_isentlevs = np.argsort(theta_levels)
    tmpk = temperature[sorter]
    isentlevels = theta_levels[sort_isentlevs]

    # Make the desired isentropic levels the same shape as temperature
    isentlevs_nd = isentlevels
    isentlevs_nd = isentlevs_nd[slices]
    shape = list(temperature.shape)
    shape[axis] = isentlevels.size
    isentlevs_nd = np.broadcast_to(isentlevs_nd, shape)

    # exponent to Poisson's Equation, which is imported above
    ka = kappa.to('dimensionless').m

    # calculate theta for each point
    pres_theta = potential_temperature(levs, tmpk)

    # Raise error if input theta level is larger than pres_theta max
    if np.max(pres_theta.m) < np.max(theta_levels):
        raise ValueError('Input theta level out of data bounds')

    # Find log of pressure to implement assumption of linear temperature dependence on
    # ln(p)
    log_p = np.log(levs.m)

    # Calculations for interpolation routine
    pok = P0 ** ka

    # index values for each point for the pressure level nearest to the desired theta level
    minv = np.apply_along_axis(np.searchsorted, axis, pres_theta.m, theta_levels)

    # Create index values for broadcasting arrays
    above = broadcast_indices(tmpk, minv, ndim, axis)
    below = broadcast_indices(tmpk, minv - 1, ndim, axis)

    # calculate constants for the interpolation
    a = (tmpk.m[above] - tmpk.m[below]) / (log_p[above] - log_p[below])
    b = tmpk.m[above] - a * log_p[above]

    # calculate first guess for interpolation
    first_guess = 0.5 * (log_p[above] + log_p[below])

    # iterative interpolation using scipy.optimize.fixed_point and _isen_iter defined above
    log_p_solved = so.fixed_point(_isen_iter, first_guess, args=(isentlevs_nd, ka, a, b,
                                                                 pok.m),
                                  xtol=eps, maxiter=max_iters)

    # get back pressure and assign nan for values with pressure greater than 1000 hPa
    isentprs = np.exp(log_p_solved)
    isentprs[isentprs > np.max(pressure.m)] = np.nan

    # create list for storing output data
    ret = []
    ret.append(isentprs * units.hPa)

    # if tmpk_out = true, calculate temperature and output as last item in list
    if tmpk_out:
        ret.append((isentlevs_nd / ((P0.m / isentprs) ** ka)) * units.kelvin)

    # check to see if any additional arguments were given, if so, interpolate to
    # new isentropic levels
    try:
        args[0]
    except IndexError:
        return ret
    else:
        # do an interpolation for each additional argument
        for arr in args:
            var = arr[sorter]
            # interpolate to isentropic levels and add to temporary output array
            arg_out = interp(isentlevels, pres_theta.m, var, axis=axis)
            ret.append(arg_out)

    # output values as a list
    return ret