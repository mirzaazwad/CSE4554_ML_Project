def is_hidden(path):
    """Return whether or not a file is hidden. `path` should be a
    bytestring filename.

    This method works differently depending on the platform it is called on.

    On OS X, it uses both the result of `is_hidden_osx` and `is_hidden_dot` to
    work out if a file is hidden.

    On Windows, it uses the result of `is_hidden_win` to work out if a file is
    hidden.

    On any other operating systems (i.e. Linux), it uses `is_hidden_dot` to
    work out if a file is hidden.
    """
    # Run platform specific functions depending on the platform
    if sys.platform == 'darwin':
        return _is_hidden_osx(path) or _is_hidden_dot(path)
    elif sys.platform == 'win32':
        return _is_hidden_win(path)
    else:
        return _is_hidden_dot(path)