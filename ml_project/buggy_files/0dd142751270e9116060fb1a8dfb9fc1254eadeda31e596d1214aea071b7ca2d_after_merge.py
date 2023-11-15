    def event(self, chunk_ret):
        '''
        Fire an event on the master bus
        '''
        if not self.opts.get('local') and self.opts.get('state_events', True):
            tag = salt.utils.event.tagify(
                    [self.jid, 'prog', self.opts['id'], str(chunk_ret['__run_num__'])], 'job'
                    )
            preload = {'jid': self.jid}
            self.functions['event.fire_master'](chunk_ret, tag, preload=preload)