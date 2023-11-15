    def visit_Str(self, node):
        '''Visitor for AST String nodes

        add relevant information about node to
        the context for use in tests which inspect strings.
        :param node: The node that is being inspected
        :return: -
        '''
        self.context['str'] = node.s
        if not isinstance(node._bandit_parent, ast.Expr):  # docstring
            self.context['linerange'] = b_utils.linerange_fix(
                node._bandit_parent
            )
            self.update_scores(self.tester.run_tests(self.context, 'Str'))