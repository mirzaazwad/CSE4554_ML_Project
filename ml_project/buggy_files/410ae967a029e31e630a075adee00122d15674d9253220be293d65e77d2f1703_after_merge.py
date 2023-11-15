def symlink(
        name,
        target,
        force=False,
        backupname=None,
        makedirs=False,
        user=None,
        group=None,
        mode=None,
        **kwargs):
    '''
    Create a symbolic link (symlink, soft link)

    If the file already exists and is a symlink pointing to any location other
    than the specified target, the symlink will be replaced. If the symlink is
    a regular file or directory then the state will return False. If the
    regular file or directory is desired to be replaced with a symlink pass
    force: True, if it is to be renamed, pass a backupname.

    name
        The location of the symlink to create

    target
        The location that the symlink points to

    force
        If the name of the symlink exists and is not a symlink and
        force is set to False, the state will fail. If force is set to
        True, the file or directory in the way of the symlink file
        will be deleted to make room for the symlink, unless
        backupname is set, when it will be renamed

    backupname
        If the name of the symlink exists and is not a symlink, it will be
        renamed to the backupname. If the backupname already
        exists and force is False, the state will fail. Otherwise, the
        backupname will be removed first.
        An absolute path OR a basename file/directory name must be provided.
        The latter will be placed relative to the symlink destination's parent
        directory.

    makedirs
        If the location of the symlink does not already have a parent directory
        then the state will fail, setting makedirs to True will allow Salt to
        create the parent directory

    user
        The user to own the file, this defaults to the user salt is running as
        on the minion

    group
        The group ownership set for the file, this defaults to the group salt
        is running as on the minion. On Windows, this is ignored

    mode
        The permissions to set on this file, aka 644, 0775, 4664. Not supported
        on Windows.

        The default mode for new files and directories corresponds umask of salt
        process. For existing files and directories it's not enforced.
    '''
    name = os.path.expanduser(name)

    # Make sure that leading zeros stripped by YAML loader are added back
    mode = salt.utils.files.normalize_mode(mode)

    user = _test_owner(kwargs, user=user)
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': ''}
    if not name:
        return _error(ret, 'Must provide name to file.symlink')

    if user is None:
        user = __opts__['user']

    if salt.utils.platform.is_windows():

        # Make sure the user exists in Windows
        # Salt default is 'root'
        if not __salt__['user.info'](user):
            # User not found, use the account salt is running under
            # If username not found, use System
            user = __salt__['user.current']()
            if not user:
                user = 'SYSTEM'

        if group is not None:
            log.warning(
                'The group argument for {0} has been ignored as this '
                'is a Windows system.'.format(name)
            )
        group = user

    if group is None:
        group = __salt__['file.gid_to_group'](
            __salt__['user.info'](user).get('gid', 0)
        )

    preflight_errors = []
    uid = __salt__['file.user_to_uid'](user)
    gid = __salt__['file.group_to_gid'](group)

    if uid == '':
        preflight_errors.append('User {0} does not exist'.format(user))

    if gid == '':
        preflight_errors.append('Group {0} does not exist'.format(group))

    if not os.path.isabs(name):
        preflight_errors.append(
            'Specified file {0} is not an absolute path'.format(name)
        )

    if preflight_errors:
        msg = '. '.join(preflight_errors)
        if len(preflight_errors) > 1:
            msg += '.'
        return _error(ret, msg)

    presult, pcomment, ret['pchanges'] = _symlink_check(name,
                                                        target,
                                                        force,
                                                        user,
                                                        group)
    if __opts__['test']:
        ret['result'] = presult
        ret['comment'] = pcomment
        return ret

    if not os.path.isdir(os.path.dirname(name)):
        if makedirs:
            __salt__['file.makedirs'](
                name,
                user=user,
                group=group,
                mode=mode)
        else:
            return _error(
                ret,
                'Directory {0} for symlink is not present'.format(
                    os.path.dirname(name)
                )
            )
    if __salt__['file.is_link'](name):
        # The link exists, verify that it matches the target
        if os.path.normpath(__salt__['file.readlink'](name)) != os.path.normpath(target):
            # The target is wrong, delete the link
            os.remove(name)
        else:
            if _check_symlink_ownership(name, user, group):
                # The link looks good!
                ret['comment'] = ('Symlink {0} is present and owned by '
                                  '{1}:{2}'.format(name, user, group))
            else:
                if _set_symlink_ownership(name, user, group):
                    ret['comment'] = ('Set ownership of symlink {0} to '
                                      '{1}:{2}'.format(name, user, group))
                    ret['changes']['ownership'] = '{0}:{1}'.format(user, group)
                else:
                    ret['result'] = False
                    ret['comment'] += (
                        'Failed to set ownership of symlink {0} to '
                        '{1}:{2}'.format(name, user, group)
                    )
            return ret

    elif os.path.isfile(name) or os.path.isdir(name):
        # It is not a link, but a file or dir
        if backupname is not None:
            if not os.path.isabs(backupname):
                if backupname == os.path.basename(backupname):
                    backupname = os.path.join(
                        os.path.dirname(os.path.normpath(name)),
                        backupname)
                else:
                    return _error(ret, (('Backupname must be an absolute path '
                                         'or a file name: {0}').format(backupname)))
            # Make a backup first
            if os.path.lexists(backupname):
                if not force:
                    return _error(ret, (('Symlink & backup dest exists and Force not set.'
                                         ' {0} -> {1} - backup: {2}').format(
                                             name, target, backupname)))
                else:
                    __salt__['file.remove'](backupname)
            try:
                __salt__['file.move'](name, backupname)
            except Exception as exc:
                ret['changes'] = {}
                log.debug(
                    'Encountered error renaming %s to %s',
                    name, backupname, exc_info=True
                )
                return _error(ret, ('Unable to rename {0} to backup {1} -> '
                                    ': {2}'.format(name, backupname, exc)))
        elif force:
            # Remove whatever is in the way
            if __salt__['file.is_link'](name):
                __salt__['file.remove'](name)
                ret['changes']['forced'] = 'Symlink was forcibly replaced'
            else:
                __salt__['file.remove'](name)
        else:
            # Otherwise throw an error
            if os.path.isfile(name):
                return _error(ret,
                              ('File exists where the symlink {0} should be'
                               .format(name)))
            else:
                return _error(ret, ((
                                        'Directory exists where the symlink {0} should be'
                                    ).format(name)))

    if not os.path.exists(name):
        # The link is not present, make it
        try:
            __salt__['file.symlink'](target, name)
        except OSError as exc:
            ret['result'] = False
            ret['comment'] = ('Unable to create new symlink {0} -> '
                              '{1}: {2}'.format(name, target, exc))
            return ret
        else:
            ret['comment'] = ('Created new symlink {0} -> '
                              '{1}'.format(name, target))
            ret['changes']['new'] = name

        if not _check_symlink_ownership(name, user, group):
            if not _set_symlink_ownership(name, user, group):
                ret['result'] = False
                ret['comment'] += (', but was unable to set ownership to '
                                   '{0}:{1}'.format(user, group))
    return ret