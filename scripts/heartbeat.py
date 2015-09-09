import os
import time
import syslog


class HeartbeatFile(object):

    def __init__(self, heartbeat_file):
        self.heartbeat_file = heartbeat_file

    def register_heartbeat(self):
        """Touch heartbeat_file or die."""
        try:
            with open(self.heartbeat_file, 'a'):
                os.utime(self.heartbeat_file, None)
        except IOError:
            syslog.syslog(syslog.LOG_ERR, "Could not update heartbeat file %s." %
                          self.heartbeat_file)
            raise

    def heartbeat_ok(self, time_limit):
        """Create and incident if the heartbeat time is too old."""
        try:
            modified_time = os.path.getmtime(self.heartbeat_file)
        except OSError:
            syslog.syslog(syslog.LOG_ERR, "Failed to check heartbeat_file %s" % self.heartbeat_file)
            raise

        heartbeat_age = int(time.time() - modified_time)

        if(heartbeat_age > time_limit):
            return False

        return True
