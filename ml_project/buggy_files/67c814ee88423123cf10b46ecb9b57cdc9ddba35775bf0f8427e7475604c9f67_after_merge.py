def finalize_spec(spec, shape):
  return tuple(_parse_lit(d) if e is _monomorphic_dim else e
               for e, d in zip(spec, shape))