def _find_install_targets(name=None,
                          version=None,
                          pkgs=None,
                          sources=None,
                          skip_suggestions=False,
                          pkg_verify=False,
                          normalize=True,
                          ignore_epoch=False,
                          reinstall=False,
                          refresh=False,
                          **kwargs):
    '''
    Inspect the arguments to pkg.installed and discover what packages need to
    be installed. Return a dict of desired packages
    '''
    was_refreshed = False

    if all((pkgs, sources)):
        return {'name': name,
                'changes': {},
                'result': False,
                'comment': 'Only one of "pkgs" and "sources" is permitted.'}

    # dict for packages that fail pkg.verify and their altered files
    altered_files = {}
    # Get the ignore_types list if any from the pkg_verify argument
    if isinstance(pkg_verify, list) \
            and any(x.get('ignore_types') is not None
                    for x in pkg_verify
                    if isinstance(x, _OrderedDict)
                    and 'ignore_types' in x):
        ignore_types = next(x.get('ignore_types')
                            for x in pkg_verify
                            if 'ignore_types' in x)
    else:
        ignore_types = []

    # Get the verify_options list if any from the pkg_verify argument
    if isinstance(pkg_verify, list) \
            and any(x.get('verify_options') is not None
                    for x in pkg_verify
                    if isinstance(x, _OrderedDict)
                    and 'verify_options' in x):
        verify_options = next(x.get('verify_options')
                            for x in pkg_verify
                            if 'verify_options' in x)
    else:
        verify_options = []

    if __grains__['os'] == 'FreeBSD':
        kwargs['with_origin'] = True

    if salt.utils.is_windows():
        # Windows requires a refresh to establish a pkg db if refresh=True, so
        # add it to the kwargs.
        kwargs['refresh'] = refresh

    try:
        cur_pkgs = __salt__['pkg.list_pkgs'](versions_as_list=True, **kwargs)
    except CommandExecutionError as exc:
        return {'name': name,
                'changes': {},
                'result': False,
                'comment': exc.strerror}

    if salt.utils.is_windows() and kwargs.pop('refresh', False):
        # We already refreshed when we called pkg.list_pkgs
        was_refreshed = True
        refresh = False

    if any((pkgs, sources)):
        if pkgs:
            desired = _repack_pkgs(pkgs)
        elif sources:
            desired = __salt__['pkg_resource.pack_sources'](
                sources,
                normalize=normalize,
            )

        if not desired:
            # Badly-formatted SLS
            return {'name': name,
                    'changes': {},
                    'result': False,
                    'comment': 'Invalidly formatted \'{0}\' parameter. See '
                               'minion log.'.format('pkgs' if pkgs
                                                    else 'sources')}
        to_unpurge = _find_unpurge_targets(desired)
    else:
        if salt.utils.is_windows():
            pkginfo = _get_package_info(name, saltenv=kwargs['saltenv'])
            if not pkginfo:
                return {'name': name,
                        'changes': {},
                        'result': False,
                        'comment': 'Package {0} not found in the '
                                   'repository.'.format(name)}
            if version is None:
                version = _get_latest_pkg_version(pkginfo)

        if normalize:
            _normalize_name = \
                __salt__.get('pkg.normalize_name', lambda pkgname: pkgname)
            desired = {_normalize_name(name): version}
        else:
            desired = {name: version}

        to_unpurge = _find_unpurge_targets(desired)

        # FreeBSD pkg supports `openjdk` and `java/openjdk7` package names
        origin = bool(re.search('/', name))

        if __grains__['os'] == 'FreeBSD' and origin:
            cver = [k for k, v in six.iteritems(cur_pkgs)
                    if v['origin'] == name]
        else:
            cver = cur_pkgs.get(name, [])

        if name not in to_unpurge:
            if version and version in cver \
                    and not reinstall \
                    and not pkg_verify:
                # The package is installed and is the correct version
                return {'name': name,
                        'changes': {},
                        'result': True,
                        'comment': 'Version {0} of package \'{1}\' is already '
                                   'installed'.format(version, name)}

            # if cver is not an empty string, the package is already installed
            elif cver and version is None \
                    and not reinstall \
                    and not pkg_verify:
                # The package is installed
                return {'name': name,
                        'changes': {},
                        'result': True,
                        'comment': 'Package {0} is already '
                                   'installed'.format(name)}

    version_spec = False
    if not sources:
        # Check for alternate package names if strict processing is not
        # enforced. Takes extra time. Disable for improved performance
        if not skip_suggestions:
            # Perform platform-specific pre-flight checks
            not_installed = dict([
                (name, version)
                for name, version in desired.items()
                if not (name in cur_pkgs and version in (None, cur_pkgs[name]))
            ])
            if not_installed:
                try:
                    problems = _preflight_check(not_installed, **kwargs)
                except CommandExecutionError:
                    pass
                else:
                    comments = []
                    if problems.get('no_suggest'):
                        comments.append(
                            'The following package(s) were not found, and no '
                            'possible matches were found in the package db: '
                            '{0}'.format(
                                ', '.join(sorted(problems['no_suggest']))
                            )
                        )
                    if problems.get('suggest'):
                        for pkgname, suggestions in \
                                six.iteritems(problems['suggest']):
                            comments.append(
                                'Package \'{0}\' not found (possible matches: '
                                '{1})'.format(pkgname, ', '.join(suggestions))
                            )
                    if comments:
                        if len(comments) > 1:
                            comments.append('')
                        return {'name': name,
                                'changes': {},
                                'result': False,
                                'comment': '. '.join(comments).rstrip()}

    # Resolve the latest package version for any packages with "latest" in the
    # package version
    wants_latest = [] \
        if sources \
        else [x for x, y in six.iteritems(desired) if y == 'latest']
    if wants_latest:
        resolved_latest = __salt__['pkg.latest_version'](*wants_latest,
                                                         refresh=refresh,
                                                         **kwargs)
        if len(wants_latest) == 1:
            resolved_latest = {wants_latest[0]: resolved_latest}
        if refresh:
            was_refreshed = True
            refresh = False

        # pkg.latest_version returns an empty string when the package is
        # up-to-date. So check the currently-installed packages. If found, the
        # resolved latest version will be the currently installed one from
        # cur_pkgs. If not found, then the package doesn't exist and the
        # resolved latest version will be None.
        for key in resolved_latest:
            if not resolved_latest[key]:
                if key in cur_pkgs:
                    resolved_latest[key] = cur_pkgs[key][-1]
                else:
                    resolved_latest[key] = None
        # Update the desired versions with the ones we resolved
        desired.update(resolved_latest)

    # Find out which packages will be targeted in the call to pkg.install
    targets = {}
    to_reinstall = {}
    problems = []
    warnings = []
    failed_verify = False
    for key, val in six.iteritems(desired):
        cver = cur_pkgs.get(key, [])
        # Package not yet installed, so add to targets
        if not cver:
            targets[key] = val
            continue
        if sources:
            if reinstall:
                to_reinstall[key] = val
                continue
            elif 'lowpkg.bin_pkg_info' not in __salt__:
                continue
            # Metadata parser is available, cache the file and derive the
            # package's name and version
            err = 'Unable to cache {0}: {1}'
            try:
                cached_path = __salt__['cp.cache_file'](val, saltenv=kwargs['saltenv'])
            except CommandExecutionError as exc:
                problems.append(err.format(val, exc))
                continue
            if not cached_path:
                problems.append(err.format(val, 'file not found'))
                continue
            elif not os.path.exists(cached_path):
                problems.append('{0} does not exist on minion'.format(val))
                continue
            source_info = __salt__['lowpkg.bin_pkg_info'](cached_path)
            if source_info is None:
                warnings.append('Failed to parse metadata for {0}'.format(val))
                continue
            else:
                oper = '=='
                verstr = source_info['version']
        else:
            if reinstall:
                to_reinstall[key] = val
                continue
            if not __salt__['pkg_resource.check_extra_requirements'](key, val):
                targets[key] = val
                continue
            # No version specified and pkg is installed
            elif __salt__['pkg_resource.version_clean'](val) is None:
                if (not reinstall) and pkg_verify:
                    try:
                        verify_result = __salt__['pkg.verify'](
                            key,
                            ignore_types=ignore_types,
                            verify_options=verify_options
                        )
                    except (CommandExecutionError, SaltInvocationError) as exc:
                        failed_verify = exc.strerror
                        continue
                    if verify_result:
                        to_reinstall[key] = val
                        altered_files[key] = verify_result
                continue
            try:
                oper, verstr = _get_comparison_spec(val)
            except CommandExecutionError as exc:
                problems.append(exc.strerror)
                continue

        # Compare desired version against installed version.
        version_spec = True
        if not sources and 'allow_updates' in kwargs:
            if kwargs['allow_updates']:
                oper = '>='
        if not _fulfills_version_spec(cver, oper, verstr,
                                      ignore_epoch=ignore_epoch):
            if reinstall:
                to_reinstall[key] = val
            elif pkg_verify and oper == '==':
                try:
                    verify_result = __salt__['pkg.verify'](
                        key,
                        ignore_types=ignore_types,
                        verify_options=verify_options)
                except (CommandExecutionError, SaltInvocationError) as exc:
                    failed_verify = exc.strerror
                    continue
                if verify_result:
                    to_reinstall[key] = val
                    altered_files[key] = verify_result
            else:
                log.debug(
                    'Current version ({0}) did not match desired version '
                    'specification ({1}), adding to installation targets'
                    .format(cver, val)
                )
                targets[key] = val

    if failed_verify:
        problems.append(failed_verify)

    if problems:
        return {'name': name,
                'changes': {},
                'result': False,
                'comment': ' '.join(problems)}

    if not any((targets, to_unpurge, to_reinstall)):
        # All specified packages are installed
        msg = 'All specified packages are already installed{0}'
        msg = msg.format(
            ' and are at the desired version' if version_spec and not sources
            else ''
        )
        return {'name': name,
                'changes': {},
                'result': True,
                'comment': msg}

    return (desired, targets, to_unpurge, to_reinstall, altered_files,
            warnings, was_refreshed)