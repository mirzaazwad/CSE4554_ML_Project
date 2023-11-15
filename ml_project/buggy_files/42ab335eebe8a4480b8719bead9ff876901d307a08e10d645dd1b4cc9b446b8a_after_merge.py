def check_if_kite_running():
    """Detect if kite is running."""
    running = False
    try:
        for proc in psutil.process_iter(attrs=['pid', 'name', 'username',
                                               'status']):
            if is_proc_kite(proc):
                logger.debug('Kite process already '
                             'running with PID {0}'.format(proc.pid))
                running = True
                break
    except OSError:
        # Needed to handle a possible WinError 0. See spyder-ide/spyder#12510
        pass
    return running