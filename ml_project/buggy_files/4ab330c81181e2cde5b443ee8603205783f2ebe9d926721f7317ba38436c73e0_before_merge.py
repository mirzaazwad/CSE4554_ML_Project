    def __init__(self, filename=None, sessionid=None, buffersize=100, gc=True, **meta):
        """Represents a xonsh session's history as an in-memory buffer that is
        periodically flushed to disk.

        Parameters
        ----------
        filename : str, optional
            Location of history file, defaults to
            ``$XONSH_DATA_DIR/xonsh-{sessionid}.json``.
        sessionid : int, uuid, str, optional
            Current session identifier, will generate a new sessionid if not
            set.
        buffersize : int, optional
            Maximum buffersize in memory.
        meta : optional
            Top-level metadata to store along with the history. The kwargs
            'cmds' and 'sessionid' are not allowed and will be overwritten.
        gc : bool, optional
            Run garbage collector flag.
        """
        super().__init__(sessionid=sessionid, **meta)
        if filename is None:
            # pylint: disable=no-member
            data_dir = builtins.__xonsh__.env.get("XONSH_DATA_DIR")
            data_dir = os.path.expanduser(data_dir)
            self.filename = os.path.join(
                data_dir, "xonsh-{0}.json".format(self.sessionid)
            )
        else:
            self.filename = filename
        self.buffer = []
        self.buffersize = buffersize
        self._queue = collections.deque()
        self._cond = threading.Condition()
        self._len = 0
        self.last_cmd_out = None
        self.last_cmd_rtn = None
        meta["cmds"] = []
        meta["sessionid"] = str(self.sessionid)
        with open(self.filename, "w", newline="\n") as f:
            xlj.ljdump(meta, f, sort_keys=True)
        self.gc = JsonHistoryGC() if gc else None
        # command fields that are known
        self.tss = JsonCommandField("ts", self)
        self.inps = JsonCommandField("inp", self)
        self.outs = JsonCommandField("out", self)
        self.rtns = JsonCommandField("rtn", self)