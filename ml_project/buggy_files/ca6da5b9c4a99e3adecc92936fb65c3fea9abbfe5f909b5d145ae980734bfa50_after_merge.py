def custom_jvp(fwd, jvp):
  @wraps(fwd)
  def fun_(*args, **kwargs):
    args_flat, in_tree = tree_flatten((args, kwargs))
    flat_fun, out_data = _flatten_fun_and_count_res(lu.wrap_init(fwd), in_tree)
    out_flat = custom_jvp_call(flat_fun, *args_flat, out_data=out_data, jvp=jvp,
                               in_tree=in_tree, keep_res=False)
    ans_tree, _, _ = out_data()
    return tree_unflatten(ans_tree, out_flat)
  return fun_