def url_handler(bot, trigger):
    """Checks for malicious URLs"""
    check = True    # Enable URL checking
    strict = False  # Strict mode: kick on malicious URL
    positives = 0   # Number of engines saying it's malicious
    total = 0       # Number of total engines
    use_vt = True   # Use VirusTotal
    check = bot.config.safety.enabled_by_default
    if check is None:
        # If not set, assume default
        check = True
    # DB overrides config:
    setting = bot.db.get_channel_value(trigger.sender, 'safety')
    if setting is not None:
        if setting == 'off':
            return  # Not checking
        elif setting in ['on', 'strict', 'local', 'local strict']:
            check = True
        if setting == 'strict' or setting == 'local strict':
            strict = True
        if setting == 'local' or setting == 'local strict':
            use_vt = False

    if not check:
        return  # Not overridden by DB, configured default off

    try:
        netloc = urlparse(trigger.group(1)).netloc
    except ValueError:
        return  # Invalid IPv6 URL

    if any(regex.search(netloc) for regex in known_good):
        return  # Whitelisted

    apikey = bot.config.safety.vt_api_key
    try:
        if apikey is not None and use_vt:
            payload = {'resource': unicode(trigger),
                       'apikey': apikey,
                       'scan': '1'}

            if trigger not in bot.memory['safety_cache']:
                r = requests.post(vt_base_api_url + 'report', data=payload)
                r.raise_for_status()
                result = r.json()
                fetched = time.time()
                data = {'positives': result['positives'],
                        'total': result['total'],
                        'fetched': fetched}
                bot.memory['safety_cache'][trigger] = data
                if len(bot.memory['safety_cache']) >= (2 * cache_limit):
                    _clean_cache(bot)
            else:
                print('using cache')
                result = bot.memory['safety_cache'][trigger]
            positives = result['positives']
            total = result['total']
    except requests.exceptions.RequestException:
        # Ignoring exceptions with VT so MalwareDomains will always work
        LOGGER.debug('[VirusTotal] Error obtaining response.', exc_info=True)
    except InvalidJSONResponse:
        # Ignoring exceptions with VT so MalwareDomains will always work
        LOGGER.debug('[VirusTotal] Malformed response (invalid JSON).', exc_info=True)

    if unicode(netloc).lower() in malware_domains:
        # malwaredomains is more trustworthy than some VT engines
        # therefore it gets a weight of 10 engines when calculating confidence
        positives += 10
        total += 10

    if positives > 1:
        # Possibly malicious URL detected!
        confidence = '{}%'.format(round((positives / total) * 100))
        msg = 'link posted by %s is possibly malicious ' % bold(trigger.nick)
        msg += '(confidence %s - %s/%s)' % (confidence, positives, total)
        bot.say('[' + bold(color('WARNING', 'red')) + '] ' + msg)
        if strict:
            bot.kick(trigger.nick, trigger.sender, 'Posted a malicious link')