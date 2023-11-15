def _hval(value):
    value = value if isinstance(value, unicode) else str(value)
    if '\n' in value or '\r' in value or '\0' in value:
        raise ValueError("Header value must not contain control characters: %r" % value)
    return value