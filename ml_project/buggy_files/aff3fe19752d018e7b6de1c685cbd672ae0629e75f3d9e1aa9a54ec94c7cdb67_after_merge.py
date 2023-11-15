def create_https_certificates(ssl_cert, ssl_key):
    """
    Create self-signed HTTPS certificares and store in paths 'ssl_cert' and 'ssl_key'

    :param ssl_cert: Path of SSL certificate file to write
    :param ssl_key: Path of SSL keyfile to write
    :return: True on success, False on failure
    """

    # assert isinstance(ssl_key, unicode)
    # assert isinstance(ssl_cert, unicode)

    try:
        # noinspection PyUnresolvedReferences
        from OpenSSL import crypto
        from certgen import createKeyPair, createCertRequest, createCertificate, TYPE_RSA
    except Exception:
        logger.log("pyopenssl module missing, please install for https access", logger.WARNING)
        return False

    import time
    serial = int(time.time())
    validity_period = (0, 60 * 60 * 24 * 365 * 10)  # ten years
    # Create the CA Certificate
    cakey = createKeyPair(TYPE_RSA, 4096)
    careq = createCertRequest(cakey, CN='Certificate Authority')
    cacert = createCertificate(careq, (careq, cakey), serial, validity_period, 'sha256')

    cname = 'SickRage'
    pkey = createKeyPair(TYPE_RSA, 4096)
    req = createCertRequest(pkey, CN=cname)
    cert = createCertificate(req, (cacert, cakey), serial, validity_period, 'sha256')

    # Save the key and certificate to disk
    try:
        # pylint: disable=no-member
        # Module has no member
        io.open(ssl_key, 'wb').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey))
        io.open(ssl_cert, 'wb').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    except Exception:
        logger.log("Error creating SSL key and certificate", logger.ERROR)
        return False

    return True