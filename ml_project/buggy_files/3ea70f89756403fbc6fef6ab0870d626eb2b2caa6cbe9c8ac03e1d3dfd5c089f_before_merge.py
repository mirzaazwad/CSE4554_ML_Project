    def __init__(self, fname, outdir, aliases, strip, install_name_mappings, install_rpath, install_mode):
        self.fname = fname
        self.outdir = outdir
        self.aliases = aliases
        self.strip = strip
        self.install_name_mappings = install_name_mappings
        self.install_rpath = install_rpath
        self.install_mode = install_mode