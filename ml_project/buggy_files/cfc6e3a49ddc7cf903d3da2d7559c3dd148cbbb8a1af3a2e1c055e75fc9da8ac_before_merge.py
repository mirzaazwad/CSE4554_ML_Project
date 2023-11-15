def prepare_context(ctx, config, verbose):
    if ctx.obj is not None:
        return

    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    ctx.obj = {}
    try:
        ctx.obj['conf'] = conf = get_config(config)
    except InvalidSettingsError:
        sys.exit(1)

    logger.debug('khal %s' % __version__)
    logger.debug('Using config:')
    logger.debug(to_unicode(stringify_conf(conf), 'utf-8'))

    if conf is None:
        raise click.UsageError('Invalid config file, exiting.')