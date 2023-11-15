    def wrapped(self, *args, **kwargs):
        remaining_tries = int(C.ANSIBLE_SSH_RETRIES) + 1
        cmd_summary = "%s..." % args[0]
        for attempt in range(remaining_tries):
            try:
                try:
                    return_tuple = func(self, *args, **kwargs)
                    display.vvv(return_tuple, host=self.host)
                    # 0 = success
                    # 1-254 = remote command return code
                    # 255 = failure from the ssh command itself
                except (AnsibleControlPersistBrokenPipeError) as e:
                    # Retry one more time because of the ControlPersist broken pipe (see #16731)
                    display.vvv(u"RETRYING BECAUSE OF CONTROLPERSIST BROKEN PIPE")
                    return_tuple = func(self, *args, **kwargs)

                if return_tuple[0] != 255:
                    break
                else:
                    raise AnsibleConnectionFailure("Failed to connect to the host via ssh: %s" % to_native(return_tuple[2]))
            except (AnsibleConnectionFailure, Exception) as e:
                if attempt == remaining_tries - 1:
                    raise
                else:
                    pause = 2 ** attempt - 1
                    if pause > 30:
                        pause = 30

                    if isinstance(e, AnsibleConnectionFailure):
                        msg = "ssh_retry: attempt: %d, ssh return code is 255. cmd (%s), pausing for %d seconds" % (attempt, cmd_summary, pause)
                    else:
                        msg = "ssh_retry: attempt: %d, caught exception(%s) from cmd (%s), pausing for %d seconds" % (attempt, e, cmd_summary, pause)

                    display.vv(msg, host=self.host)

                    time.sleep(pause)
                    continue

        return return_tuple