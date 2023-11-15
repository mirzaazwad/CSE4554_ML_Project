    def current_window(self, keyctx):
        """
        Returns the active window with a matching key context, ignoring overlays.
        If multiple stacks have an active widget with a matching key context,
        the currently focused stack is preferred.
        """
        for s in self.stacks_sorted_by_focus():
            t = s.top_window()
            if t.keyctx == keyctx:
                return t