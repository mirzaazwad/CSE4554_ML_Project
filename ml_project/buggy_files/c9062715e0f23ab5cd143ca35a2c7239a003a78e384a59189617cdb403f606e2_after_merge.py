    def to_representation(self, page):
        if page.specific_class is None:
            return None
        name = page.specific_class._meta.app_label + '.' + page.specific_class.__name__
        self.context['view'].seen_types[name] = page.specific_class
        return name