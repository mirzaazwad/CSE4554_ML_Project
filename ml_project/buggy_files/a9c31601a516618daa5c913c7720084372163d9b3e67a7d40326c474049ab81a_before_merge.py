    def _poly(expr, opt):
        terms, poly_terms = [], []

        for term in Add.make_args(expr):
            factors, poly_factors = [], []

            for factor in Mul.make_args(term):
                if factor.is_Add:
                    poly_factors.append(_poly(factor, opt))
                elif factor.is_Pow and factor.base.is_Add and factor.exp.is_Integer:
                    poly_factors.append(
                        _poly(factor.base, opt).pow(factor.exp))
                else:
                    factors.append(factor)

            if not poly_factors:
                terms.append(term)
            else:
                product = poly_factors[0]

                for factor in poly_factors[1:]:
                    product = product.mul(factor)

                if factors:
                    factor = Mul(*factors)

                    if factor.is_Number:
                        product = product.mul(factor)
                    else:
                        product = product.mul(Poly._from_expr(factor, opt))

                poly_terms.append(product)

        if not poly_terms:
            result = Poly._from_expr(expr, opt)
        else:
            result = poly_terms[0]

            for term in poly_terms[1:]:
                result = result.add(term)

            if terms:
                term = Add(*terms)

                if term.is_Number:
                    result = result.add(term)
                else:
                    result = result.add(Poly._from_expr(term, opt))

        return result.reorder(*opt.get('gens', ()), **args)