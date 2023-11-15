    def build_typeddict_typeinfo(self, name: str, items: List[str],
                                 types: List[Type],
                                 required_keys: Set[str]) -> TypeInfo:
        fallback = (self.named_type_or_none('typing.Mapping',
                                            [self.str_type(), self.object_type()])
                    or self.object_type())

        def patch() -> None:
            # Calculate the correct value type for the fallback Mapping.
            fallback.args[1] = join.join_type_list(types)

        # We can't calculate the complete fallback type until after semantic
        # analysis, since otherwise MROs might be incomplete. Postpone a callback
        # function that patches the fallback.
        self.patches.append(patch)

        info = self.basic_new_typeinfo(name, fallback)
        info.typeddict_type = TypedDictType(OrderedDict(zip(items, types)), required_keys,
                                            fallback)
        return info