    def provide_context_and_uptodate(self, classification, lang, node=None):
        """Provide data for the context and the uptodate list for the list of the given classifiation."""
        cat_path = self.extract_hierarchy(classification)
        kw = {
            'category_path': self.site.config['CATEGORY_PATH'],
            'category_prefix': self.site.config['CATEGORY_PREFIX'],
            "category_pages_are_indexes": self.site.config['CATEGORY_PAGES_ARE_INDEXES'],
            "tzinfo": self.site.tzinfo,
            "category_pages_descriptions": self.site.config['CATEGORY_PAGES_DESCRIPTIONS'],
            "category_pages_titles": self.site.config['CATEGORY_PAGES_TITLES'],
        }
        posts = self.site.posts_per_classification[self.classification_name][lang]
        if node is None:
            children = []
        else:
            children = [child for child in node.children if len([post for post in posts.get(child.classification_name, []) if self.site.config['SHOW_UNTRANSLATED_POSTS'] or post.is_translation_available(lang)]) > 0]
        subcats = [(child.name, self.site.link(self.classification_name, child.classification_name, lang)) for child in children]
        friendly_name = self.get_classification_friendly_name(classification, lang)
        context = {
            "title": self.site.config['CATEGORY_PAGES_TITLES'].get(lang, {}).get(classification, self.site.MESSAGES[lang]["Posts about %s"] % friendly_name),
            "description": self.site.config['CATEGORY_PAGES_DESCRIPTIONS'].get(lang, {}).get(classification),
            "pagekind": ["tag_page", "index" if self.show_list_as_index else "list"],
            "tag": friendly_name,
            "category": classification,
            "category_path": cat_path,
            "subcategories": subcats,
        }
        kw.update(context)
        return context, kw