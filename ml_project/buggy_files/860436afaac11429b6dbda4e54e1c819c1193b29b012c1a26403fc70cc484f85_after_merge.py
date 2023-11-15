    def document_did_change(self, text=None):
        """Send textDocument/didChange request to the server."""
        self.text_version += 1
        text = self.toPlainText()
        self.patch = self.differ.patch_make(self.previous_text, text)
        self.previous_text = text
        cursor = self.textCursor()
        params = {
            'file': self.filename,
            'version': self.text_version,
            'text': text,
            'diff': self.patch,
            'offset': cursor.position(),
            'selection_start': cursor.selectionStart(),
            'selection_end': cursor.selectionEnd(),
        }
        return params