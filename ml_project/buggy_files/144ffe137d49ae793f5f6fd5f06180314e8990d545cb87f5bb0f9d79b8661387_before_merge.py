def _lift_linearized(jaxpr, primal_avals, consts, io_tree, out_pvals, *py_args):
  def fun(*tangents):
    tangent_avals = list(map(core.get_aval, tangents))
    for primal_aval, tangent_aval in zip(primal_avals, tangent_avals):
      try:
        core.lattice_join(primal_aval, tangent_aval)
      except TypeError as e:
        msg = ("linearized function called on tangent values inconsistent with "
               "the original primal values.")
        raise ValueError(msg) from e
    tangents_out = eval_jaxpr(jaxpr, consts, *tangents)
    return tuple(map(lambda out_pv, tan_out: out_pv.merge_with_known(tan_out),
                     out_pvals, tangents_out))

  return apply_flat_fun(fun, io_tree, *py_args)