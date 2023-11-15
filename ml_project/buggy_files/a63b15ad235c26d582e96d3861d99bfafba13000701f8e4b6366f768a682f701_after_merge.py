    def _replace_parallel_functions(self, blocks):
        """
        Replace functions with their parallel implementation in
        replace_functions_map if available.
        The implementation code is inlined to enable more optimization.
        """
        swapped = self.swapped
        from numba.inline_closurecall import inline_closure_call
        work_list = list(blocks.items())
        while work_list:
            label, block = work_list.pop()
            for i, instr in enumerate(block.body):
                if isinstance(instr, ir.Assign):
                    lhs = instr.target
                    lhs_typ = self.typemap[lhs.name]
                    expr = instr.value
                    if isinstance(expr, ir.Expr) and expr.op == 'call':
                        # Try and inline known calls with their parallel implementations
                        def replace_func():
                            func_def = get_definition(self.func_ir, expr.func)
                            callname = find_callname(self.func_ir, expr)
                            repl_func = replace_functions_map.get(callname, None)
                            if (repl_func is None and
                                len(callname) == 2 and
                                isinstance(callname[1], ir.Var) and
                                isinstance(self.typemap[callname[1].name],
                                           types.npytypes.Array)):
                                repl_func = replace_functions_ndarray.get(callname[0], None)
                                if repl_func is not None:
                                    # Add the array that the method is on to the arg list.
                                    expr.args.insert(0, callname[1])

                            require(repl_func != None)
                            typs = tuple(self.typemap[x.name] for x in expr.args)
                            try:
                                new_func =  repl_func(lhs_typ, *typs)
                            except:
                                new_func = None
                            require(new_func != None)
                            g = copy.copy(self.func_ir.func_id.func.__globals__)
                            g['numba'] = numba
                            g['np'] = numpy
                            g['math'] = math
                            # if the function being inlined has a function
                            # checking the inputs, find it and add it to globals
                            check = replace_functions_checkers_map.get(callname,
                                                                       None)
                            if check is not None:
                                g[check.name] = check.func
                            # inline the parallel implementation
                            new_blocks, _ = inline_closure_call(self.func_ir, g,
                                            block, i, new_func, self.typingctx, typs,
                                            self.typemap, self.calltypes, work_list)
                            call_table = get_call_table(new_blocks, topological_ordering=False)

                            # find the prange in the new blocks and record it for use in diagnostics
                            for call in call_table:
                                for k, v in call.items():
                                    if v[0] == 'internal_prange':
                                        swapped[k] = [callname, repl_func.__name__, func_def, block.body[i].loc]
                                        break
                            return True
                        if guard(replace_func):
                            break
                    elif (isinstance(expr, ir.Expr) and expr.op == 'getattr' and
                          expr.attr == 'dtype'):
                        # Replace getattr call "A.dtype" with numpy.dtype(<actual type>).
                        # This helps remove superfluous dependencies from parfor.
                        typ = self.typemap[expr.value.name]
                        if isinstance(typ, types.npytypes.Array):
                            # Convert A.dtype to four statements.
                            # 1) Get numpy global.
                            # 2) Create var for known type of array as string
                            #    constant. e.g. 'float64'
                            # 3) Get dtype function from numpy module.
                            # 4) Create var for numpy.dtype(var from #2).

                            # Create var for numpy module.
                            dtype = typ.dtype
                            scope = block.scope
                            loc = instr.loc
                            g_np_var = ir.Var(scope, mk_unique_var("$np_g_var"), loc)
                            self.typemap[g_np_var.name] = types.misc.Module(numpy)
                            g_np = ir.Global('np', numpy, loc)
                            g_np_assign = ir.Assign(g_np, g_np_var, loc)

                            # Create var for the inferred type of the array
                            # e.g., 'float64'
                            dtype_str = str(dtype)
                            if dtype_str == 'bool':
                                dtype_str = 'bool_'
                            typ_var = ir.Var(
                                scope, mk_unique_var("$np_typ_var"), loc)
                            self.typemap[typ_var.name] = types.StringLiteral(
                                dtype_str)
                            typ_var_assign = ir.Assign(
                                ir.Const(dtype_str, loc), typ_var, loc)

                            # Get the dtype function from the numpy module.
                            dtype_attr_var = ir.Var(scope, mk_unique_var("$dtype_attr_var"), loc)
                            temp = find_template(numpy.dtype)
                            tfunc = numba.types.Function(temp)
                            tfunc.get_call_type(self.typingctx, (self.typemap[typ_var.name],), {})
                            self.typemap[dtype_attr_var.name] = types.functions.Function(temp)
                            dtype_attr_getattr = ir.Expr.getattr(g_np_var, 'dtype', loc)
                            dtype_attr_assign = ir.Assign(dtype_attr_getattr, dtype_attr_var, loc)

                            # Call numpy.dtype on the statically coded type two steps above.
                            dtype_var = ir.Var(scope, mk_unique_var("$dtype_var"), loc)
                            self.typemap[dtype_var.name] = types.npytypes.DType(dtype)
                            dtype_getattr = ir.Expr.call(dtype_attr_var, [typ_var], (), loc)
                            dtype_assign = ir.Assign(dtype_getattr, dtype_var, loc)
                            self.calltypes[dtype_getattr] = signature(
                                self.typemap[dtype_var.name], self.typemap[typ_var.name])

                            # The original A.dtype rhs is replaced with result of this call.
                            instr.value = dtype_var
                            # Add statements to body of the code.
                            block.body.insert(0, dtype_assign)
                            block.body.insert(0, dtype_attr_assign)
                            block.body.insert(0, typ_var_assign)
                            block.body.insert(0, g_np_assign)
                            break