    def read(self):
        data, bad_format = None, False
        try:
            data = json.loads(self.file.read_text())
            logging.debug("got {} from %s".format(self.msg), *self.msg_args)
            return data
        except ValueError:
            bad_format = True
        except Exception:  # noqa
            pass
        if bad_format:
            try:
                self.remove()
            except OSError:  # reading and writing on the same file may cause race on multiple processes
                pass
        return None