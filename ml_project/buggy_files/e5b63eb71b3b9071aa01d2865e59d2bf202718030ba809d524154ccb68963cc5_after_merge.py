def literal_stringizer(value):
    """Convert a `value` to a Python literal in GML representation.

    Parameters
    ----------
    value : object
        The `value` to be converted to GML representation.

    Returns
    -------
    rep : string
        A double-quoted Python literal representing value. Unprintable
        characters are replaced by XML character references.

    Raises
    ------
    ValueError
        If `value` cannot be converted to GML.

    Notes
    -----
    `literal_stringizer` is largely the same as `repr` in terms of
    functionality but attempts prefix `unicode` and `bytes` literals with
    `u` and `b` to provide better interoperability of data generated by
    Python 2 and Python 3.

    The original value can be recovered using the
    :func:`networkx.readwrite.gml.literal_destringizer` function.
    """
    def stringize(value):
        if isinstance(value, (int, long, bool)) or value is None:
            if value is True:  # GML uses 1/0 for boolean values.
                buf.write(str(1))
            elif value is False:
                buf.write(str(0))
            else:
                buf.write(str(value))
        elif isinstance(value, unicode):
            text = repr(value)
            if text[0] != 'u':
                try:
                    value.encode('latin1')
                except UnicodeEncodeError:
                    text = 'u' + text
            buf.write(text)
        elif isinstance(value, (float, complex, str, bytes)):
            buf.write(repr(value))
        elif isinstance(value, list):
            buf.write('[')
            first = True
            for item in value:
                if not first:
                    buf.write(',')
                else:
                    first = False
                stringize(item)
            buf.write(']')
        elif isinstance(value, tuple):
            if len(value) > 1:
                buf.write('(')
                first = True
                for item in value:
                    if not first:
                        buf.write(',')
                    else:
                        first = False
                    stringize(item)
                buf.write(')')
            elif value:
                buf.write('(')
                stringize(value[0])
                buf.write(',)')
            else:
                buf.write('()')
        elif isinstance(value, dict):
            buf.write('{')
            first = True
            for key, value in value.items():
                if not first:
                    buf.write(',')
                else:
                    first = False
                stringize(key)
                buf.write(':')
                stringize(value)
            buf.write('}')
        elif isinstance(value, set):
            buf.write('{')
            first = True
            for item in value:
                if not first:
                    buf.write(',')
                else:
                    first = False
                stringize(item)
            buf.write('}')
        else:
            raise ValueError(
                '%r cannot be converted into a Python literal' % (value,))

    buf = StringIO()
    stringize(value)
    return buf.getvalue()