    def __init__(self, name, start, check=None, listener=None):
        self.plugin_name = name
        self.start_function = start
        self.listener = listener
        self.check_function = check