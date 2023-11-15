def installed(name, default=False, runas=None, user=None):
    '''
    Verify that the specified ruby is installed with RVM. RVM is
    installed when necessary.

    name
        The version of ruby to install

    default : False
        Whether to make this ruby the default.

    runas: None
        The user to run rvm as.

        .. deprecated:: 0.17.0

    user: None
        The user to run rvm as.

        ..versionadded:: 0.17.0
    '''
    ret = {'name': name, 'result': None, 'comment': '', 'changes': {}}

    salt.utils.warn_until(
        'Hydrogen',
        'Please remove \'runas\' support at this stage. \'user\' support was '
        'added in 0.17.0',
        _dont_call_warnings=True
    )
    if runas:
        # Warn users about the deprecation
        ret.setdefault('warnings', []).append(
            'The \'runas\' argument is being deprecated in favor or \'user\', '
            'please update your state files.'
        )
    if user is not None and runas is not None:
        # user wins over runas but let warn about the deprecation.
        ret.setdefault('warnings', []).append(
            'Passed both the \'runas\' and \'user\' arguments. Please don\'t. '
            '\'runas\' is being ignored in favor of \'user\'.'
        )
        runas = None
    elif runas is not None:
        # Support old runas usage
        user = runas
        runas = None

    if __opts__['test']:
        ret['comment'] = 'Ruby {0} is set to be installed'.format(name)
        return ret

    ret = _check_rvm(ret, user)
    if ret['result'] is False:
        if not __salt__['rvm.install'](runas=user):
            ret['comment'] = 'RVM failed to install.'
            return ret
        else:
            return _check_and_install_ruby(ret, name, default, user=user)
    else:
        return _check_and_install_ruby(ret, name, default, user=user)