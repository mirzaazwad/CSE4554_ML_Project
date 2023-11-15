    def get_exit_status(self, channel):
        """Get exit status code for channel or ``None`` if not ready.

        :param channel: The channel to get status from.
        :type channel: :py:mod:`ssh.channel.Channel`
        :rtype: int or ``None``
        """
        if not channel.is_eof():
            return
        return channel.get_exit_status()