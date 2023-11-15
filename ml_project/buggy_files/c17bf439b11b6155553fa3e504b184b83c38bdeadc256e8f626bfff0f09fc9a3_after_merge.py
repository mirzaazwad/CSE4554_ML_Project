    def dialog_mode(self, dialog_mode):
        """Switch on/off the speaker's dialog mode.

        :param dialog_mode: Enable or disable dialog mode
        :type dialog_mode: bool
        :raises NotSupportedException: If the device does not support
        dialog mode.
        """
        if not self.is_soundbar:
            message = 'This device does not support dialog mode'
            raise NotSupportedException(message)

        self.renderingControl.SetEQ([
            ('InstanceID', 0),
            ('EQType', 'DialogLevel'),
            ('DesiredValue', int(dialog_mode))
        ])