    def __init__(self, pid, name=None, ppid=None, msg=None):
        Error.__init__(self)
        self.pid = pid
        self.ppid = ppid
        self.name = name
        self.msg = msg
        if msg is None:
            if name and ppid:
                details = "(pid=%s, name=%s, ppid=%s)" % (
                    self.pid, repr(self.name), self.ppid)
            elif name:
                details = "(pid=%s, name=%s)" % (self.pid, repr(self.name))
            else:
                details = "(pid=%s)" % self.pid
            self.msg = "process still exists but it's a zombie " + details