def do_unpickle(data):
    """Retrieve pickle from pickled string"""
    return loads(to_bytes(data))