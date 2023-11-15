    def __init__(self, message=None, **kwargs):
        if not message:
            message = (
                "activate_this.py not found. Your environment is most certainly "
                "not activated. Continuing anyway…"
            )
        self.message = message
        VirtualenvException.__init__(self, fix_utf8(message), **kwargs)