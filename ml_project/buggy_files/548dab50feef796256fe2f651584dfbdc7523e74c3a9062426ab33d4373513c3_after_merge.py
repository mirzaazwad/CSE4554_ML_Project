def _coerce_method(converter):
    """
    Install the scalar coercion methods.
    """

    def wrapper(self):
        if len(self) == 1:
            return converter(self.iloc[0])
        raise TypeError("cannot convert the series to "
                        "{0}".format(str(converter)))

    wrapper.__name__ = "__{name}__".format(name=converter.__name__)
    return wrapper