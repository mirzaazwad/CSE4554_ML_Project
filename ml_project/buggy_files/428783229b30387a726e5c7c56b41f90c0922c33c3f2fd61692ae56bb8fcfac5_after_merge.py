  def _receive_remote_pgrp(self, pgrp):
    self._current_remote_pgrp = pgrp
    self._maybe_write_pid_file()