    def _send_output_to_pager(self, output):
        cmdline = self.get_pager_cmdline()
        LOG.debug("Running command: %s", cmdline)
        with ignore_ctrl_c():
            # We can't rely on the KeyboardInterrupt from
            # the CLIDriver being caught because when we
            # send the output to a pager it will use various
            # control characters that need to be cleaned
            # up gracefully.  Otherwise if we simply catch
            # the Ctrl-C and exit, it will likely leave the
            # users terminals in a bad state and they'll need
            # to manually run ``reset`` to fix this issue.
            # Ignoring Ctrl-C solves this issue.  It's also
            # the default behavior of less (you can't ctrl-c
            # out of a manpage).
            p = self._popen(cmdline, stdin=PIPE)
            p.communicate(input=output)