    def symlink_list(self, load):
        '''
        Return a list of symlinked files and dirs
        '''
        if 'env' in load:
            salt.utils.warn_until(
                'Boron',
                'Passing a salt environment should be done using \'saltenv\' '
                'not \'env\'. This functionality will be removed in Salt '
                'Boron.'
            )
            load['saltenv'] = load.pop('env')

        ret = {}
        if 'saltenv' not in load:
            return {}
        for fsb in self._gen_back(load.pop('fsbackend', None)):
            symlstr = '{0}.symlink_list'.format(fsb)
            if symlstr in self.servers:
                ret = self.servers[symlstr](load)
        # upgrade all set elements to a common encoding
        ret = dict([
            (salt.utils.locales.sdecode(x), salt.utils.locales.sdecode(y)) for x, y in ret.items()
        ])
        # some *fs do not handle prefix. Ensure it is filtered
        prefix = load.get('prefix', '').strip('/')
        if prefix != '':
            ret = dict([
                (x, y) for x, y in six.iteritems(ret) if x.startswith(prefix)
            ])
        return ret