def clip(
    ctx,
    files,
    output,
    bounds,
    like,
    driver,
    projection,
    overwrite,
    creation_options,
    with_complement,
):
    """Clips a raster using projected or geographic bounds.

    \b
      $ rio clip input.tif output.tif --bounds xmin ymin xmax ymax
      $ rio clip input.tif output.tif --like template.tif

    The values of --bounds are presumed to be from the coordinate
    reference system of the input dataset unless the --geographic option
    is used, in which case the values may be longitude and latitude
    bounds. Either JSON, for example "[west, south, east, north]", or
    plain text "west south east north" representations of a bounding box
    are acceptable.

    If using --like, bounds will automatically be transformed to match the
    coordinate reference system of the input.

    It can also be combined to read bounds of a feature dataset using Fiona:

    \b
      $ rio clip input.tif output.tif --bounds $(fio info features.shp --bounds)

    """
    from rasterio.warp import transform_bounds

    with ctx.obj['env']:

        output, files = resolve_inout(files=files, output=output, overwrite=overwrite)
        input = files[0]

        with rasterio.open(input) as src:
            if bounds:
                if projection == 'geographic':
                    bounds = transform_bounds(CRS.from_epsg(4326), src.crs, *bounds)
                if disjoint_bounds(bounds, src.bounds):
                    raise click.BadParameter('must overlap the extent of '
                                             'the input raster',
                                             param='--bounds',
                                             param_hint='--bounds')
            elif like:
                with rasterio.open(like) as template_ds:
                    bounds = template_ds.bounds
                    if template_ds.crs != src.crs:
                        bounds = transform_bounds(template_ds.crs, src.crs,
                                                  *bounds)

                    if disjoint_bounds(bounds, src.bounds):
                        raise click.BadParameter('must overlap the extent of '
                                                 'the input raster',
                                                 param='--like',
                                                 param_hint='--like')

            else:
                raise click.UsageError('--bounds or --like required')

            bounds_window = src.window(*bounds)

            if not with_complement:
                bounds_window = bounds_window.intersection(
                    Window(0, 0, src.width, src.height)
                )

            # Get the window with integer height
            # and width that contains the bounds window.
            out_window = bounds_window.round_lengths(op='ceil')

            height = int(out_window.height)
            width = int(out_window.width)

            out_kwargs = src.profile
            out_kwargs.update({
                'driver': driver,
                'height': height,
                'width': width,
                'transform': src.window_transform(out_window)})
            out_kwargs.update(**creation_options)

            if 'blockxsize' in out_kwargs and out_kwargs['blockxsize'] > width:
                del out_kwargs['blockxsize']
                logger.warning("Blockxsize removed from creation options to accomodate small output width")
            if 'blockysize' in out_kwargs and out_kwargs['blockysize'] > height:
                del out_kwargs['blockysize']
                logger.warning("Blockysize removed from creation options to accomodate small output height")

            with rasterio.open(output, "w", **out_kwargs) as out:
                out.write(
                    src.read(
                        window=out_window,
                        out_shape=(src.count, height, width),
                        boundless=True,
                    )
                )