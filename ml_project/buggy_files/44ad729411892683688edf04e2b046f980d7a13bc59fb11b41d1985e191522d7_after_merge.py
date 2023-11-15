def remove_dead_block(block, lives, call_table, arg_aliases, alias_map, alias_set, typemap):
    """remove dead code using liveness info.
    Mutable arguments (e.g. arrays) that are not definitely assigned are live
    after return of function.
    """
    # TODO: find mutable args that are not definitely assigned instead of
    # assuming all args are live after return
    removed = False

    # add statements in reverse order
    new_body = [block.terminator]
    # for each statement in reverse order, excluding terminator
    for stmt in reversed(block.body[:-1]):
        # aliases of lives are also live
        alias_lives = set()
        init_alias_lives = lives & alias_set
        for v in init_alias_lives:
            alias_lives |= alias_map[v]
        # let external calls handle stmt if type matches
        for t, f in remove_dead_extensions.items():
            if isinstance(stmt, t):
                f(stmt, lives, arg_aliases, alias_map, typemap)
        # ignore assignments that their lhs is not live or lhs==rhs
        if isinstance(stmt, ir.Assign):
            lhs = stmt.target
            rhs = stmt.value
            if lhs.name not in lives and has_no_side_effect(
                    rhs, lives, call_table):
                removed = True
                continue
            if isinstance(rhs, ir.Var) and lhs.name == rhs.name:
                removed = True
                continue
            # TODO: remove other nodes like SetItem etc.
        if isinstance(stmt, ir.SetItem):
            if stmt.target.name not in lives and stmt.target.name not in alias_lives:
                continue

        if type(stmt) in analysis.ir_extension_usedefs:
            def_func = analysis.ir_extension_usedefs[type(stmt)]
            uses, defs = def_func(stmt)
            lives -= defs
            lives |= uses
        else:
            lives |= {v.name for v in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                lives.remove(lhs.name)

        new_body.append(stmt)
    new_body.reverse()
    block.body = new_body
    return removed