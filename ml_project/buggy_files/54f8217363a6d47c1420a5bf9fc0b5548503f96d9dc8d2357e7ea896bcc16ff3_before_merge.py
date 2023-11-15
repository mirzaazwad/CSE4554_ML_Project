    def __init__(self, scc, **kwds):
        super(StronglyConnectedCircularType, self).__init__(None, **kwds)
        self.scc = scc

        types = set(scc)
        for type in scc:
            self.add_children(type.children - types)
            self.add_parents(type.parents - types)

        self.types = scc
        self.promotions = set(type for type in scc if type.is_promotion)
        self.reanalyzeable = set(type for type in scc if type.is_reanalyze_circular)