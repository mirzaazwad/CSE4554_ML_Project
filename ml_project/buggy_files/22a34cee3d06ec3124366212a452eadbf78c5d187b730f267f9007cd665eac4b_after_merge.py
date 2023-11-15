    def start(self):
        '''
        Start the actual minion.

        If sub-classed, don't **ever** forget to run:

            super(YourSubClass, self).start()

        NOTE: Run any required code before calling `super()`.
        '''
        super(Minion, self).start()
        try:
            if check_user(self.config['user']):
                log.info('The salt minion is starting up')
                self.minion.tune_in()
        except (KeyboardInterrupt, SaltSystemExit) as exc:
            log.warn('Stopping the Salt Minion')
            if isinstance(exc, KeyboardInterrupt):
                log.warn('Exiting on Ctrl-c')
                self.shutdown()
            else:
                log.error(str(exc))
                self.shutdown(exc.code)