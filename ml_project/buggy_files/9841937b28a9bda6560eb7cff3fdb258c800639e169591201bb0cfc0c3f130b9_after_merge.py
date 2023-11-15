def config_checks(config):
    """do some tests on the config we cannot do with configobj's validator"""
    if len(config['calendars'].keys()) < 1:
        logger.fatal('Found no calendar section in the config file')
        raise InvalidSettingsError()
    test_default_calendar(config)
    config['sqlite']['path'] = expand_db_path(config['sqlite']['path'])
    if not config['locale']['default_timezone']:
        config['locale']['default_timezone'] = is_timezone(
            config['locale']['default_timezone'])
    if not config['locale']['local_timezone']:
        config['locale']['local_timezone'] = is_timezone(
            config['locale']['local_timezone'])