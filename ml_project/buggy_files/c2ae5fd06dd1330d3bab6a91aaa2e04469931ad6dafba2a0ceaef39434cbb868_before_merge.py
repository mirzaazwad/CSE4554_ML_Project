    def add_content(self, more_content: Optional[StringList], no_docstring: bool = False
                    ) -> None:
        if self.doc_as_attr:
            more_content = StringList([_('alias of %s') % restify(self.object)], source='')
            super().add_content(more_content, no_docstring=True)
        else:
            super().add_content(more_content)