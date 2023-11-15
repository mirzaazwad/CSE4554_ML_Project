    def populate_ddl_identity(
        self,
        schema: s_schema.Schema,
        context: sd.CommandContext,
    ) -> s_schema.Schema:
        schema = super().populate_ddl_identity(schema, context)
        if not isinstance(self, sd.CreateObject):
            anno = self.scls.get_annotation(schema)
        else:
            annoname = sn.shortname_from_fullname(self.classname)
            anno = schema.get(annoname, type=Annotation)
        self.set_ddl_identity('annotation', anno)
        return schema