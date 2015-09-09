#!/usr/bin/python

"""
Check_mk local_check that report CRITICAL if monitor_check_mk is unable to
do its job.
"""

import heartbeat

MONITOR_CHECK_MK_HEARTBEAT_FILE = '/var/tmp/monitor_check_mk_heartbeat'
HEARTBEAT_TIME_LIMIT = 600  # 10 minutes in seconds


def check_monitor_check_mk():

    try:
        heartbeatfile = heartbeat.HeartbeatFile(MONITOR_CHECK_MK_HEARTBEAT_FILE)
        if(not heartbeatfile.heartbeat_ok(HEARTBEAT_TIME_LIMIT)):
            print "2 Service_monitor_check_mk - CRITICAL - Monitor_check_mk heartbeat file is stale!"
        else:
            print "0 Service_monitor_check_mk - OK - Monitor_check_mk heartbeat file is ok!"
    except OSError:
        print "2 Service_monitor_check_mk - CRITICAL - Monitor_check_mk heartbeat file does not exist!"


if __name__ == '__main__':
    check_monitor_check_mk()
