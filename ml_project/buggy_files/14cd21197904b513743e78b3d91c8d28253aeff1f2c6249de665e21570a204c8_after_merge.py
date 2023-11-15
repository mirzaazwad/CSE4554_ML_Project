    def format(self, record):
        if record.pathname:
            record.pathname = ensure_text(record.pathname, get_filesystem_encoding())

        self._gen_rel_path(record)

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        return result