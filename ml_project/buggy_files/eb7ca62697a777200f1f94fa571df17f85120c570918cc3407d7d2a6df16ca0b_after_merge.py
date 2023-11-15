    def get_selection_bounds(self, cursor=None):
        """Return selection bounds (block numbers)."""
        if cursor is None:
            cursor = self.textCursor()
        start, end = cursor.selectionStart(), cursor.selectionEnd()
        block_start = self.document().findBlock(start)
        block_end = self.document().findBlock(end)
        return sorted([block_start.blockNumber(), block_end.blockNumber()])