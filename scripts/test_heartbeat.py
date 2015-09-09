import unittest2
import heartbeat
import os
import time

heartbeat_file = '/tmp/heartbeat_test'


def cleanup_heartbeat():
    os.remove(heartbeat_file)


class TestHeartbeatRegisterNewFile(unittest2.TestCase):
    def setUp(self):
        self.addCleanup(cleanup_heartbeat)
        self.heartbeatfile = heartbeat.HeartbeatFile(heartbeat_file)

    def test_register_heartbeat_with_new_file(self):
        self.heartbeatfile.register_heartbeat()
        self.assertTrue(os.path.isfile(heartbeat_file))


class TestHeartbeatRegisterOldFile(unittest2.TestCase):

    def setUp(self):
        self.addCleanup(cleanup_heartbeat)

        two_hours_ago = (int(time.time()) - (2*60*60))
        with open(heartbeat_file, 'a'):
            os.utime(heartbeat_file, (two_hours_ago, two_hours_ago))

        self.heartbeatfile = heartbeat.HeartbeatFile(heartbeat_file)

    def test_register_heartbeat_with_old_file(self):
        self.heartbeatfile.register_heartbeat()
        self.assertTrue(
            (os.path.getmtime(heartbeat_file) > (int(time.time())) - (2*60*60))
            )


class TestHeartbeatMonitor(unittest2.TestCase):

    def setUp(self):
        self.heartbeatfile = heartbeat.HeartbeatFile(heartbeat_file)
        self.heartbeatfile.register_heartbeat()
        self.addCleanup(cleanup_heartbeat)

    def test_heartbeat_ok(self):
        self.assertTrue(self.heartbeatfile.heartbeat_ok(2))
