def groupby_apply(groupby, func, *args, dtypes=None, index=None, output_type=None, **kwargs):
    # todo this can be done with sort_index implemented
    if not groupby.op.groupby_params.get('as_index', True):
        raise NotImplementedError('apply when set_index == False is not supported')

    output_types = kwargs.pop('output_types', None)
    object_type = kwargs.pop('object_type', None)
    output_types = validate_output_types(
        output_types=output_types, output_type=output_type, object_type=object_type)

    op = GroupByApply(func=func, args=args, kwds=kwargs, output_types=output_types)
    return op(groupby, dtypes=dtypes, index=index)