def returner(ret):
    '''
    Send an email with the data
    '''

    from_addr = __salt__['config.option']('smtp.from')
    to_addrs = __salt__['config.option']('smtp.to')
    host = __salt__['config.option']('smtp.host')
    port = __salt__['config.option']('smtp.port')
    if not port:
        port = 25
    log.debug('smtp port has been set to {0}'.format(port))
    user = __salt__['config.option']('smtp.username')
    passwd = __salt__['config.option']('smtp.password')
    subject = __salt__['config.option']('smtp.subject')

    fields = __salt__['config.option']('smtp.fields').split(',')
    for field in fields:
        if field in ret.keys():
            subject += ' {0}'.format(ret[field])
    log.debug('subject')

    content = pprint.pformat(ret['return'])
    message = ('From: {0}\r\n'
               'To: {1}\r\n'
               'Date: {2}\r\n'
               'Subject: {3}\r\n'
               '\r\n'
               'id: {4}\r\n'
               'function: {5}\r\n'
               'function args: {6}\r\n'
               'jid: {7}\r\n'
               '{8}').format(from_addr,
                             to_addrs,
                             formatdate(localtime=True),
                             subject,
                             ret['id'],
                             ret['fun'],
                             ret['fun_args'],
                             ret['jid'],
                             content)

    server = smtplib.SMTP(host, int(port))
    if __salt__['config.option']('smtp.tls') is True:
        server.starttls()
    if user and passwd:
        server.login(user, passwd)
    server.sendmail(from_addr, to_addrs, message)
    server.quit()