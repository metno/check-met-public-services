#!/usr/bin/python

"""monitor_check_mk.py is responsible for reporting to pagerduty if check_mk
is down.

monitor_check_mk considers check_mk to be down if the file
CHECK_MK_HEARTBEAT_FILE is stale.

monitor_check_mk reports its own health by touching the file
MONITOR_CHECK_MK_HEARTBEAT_FILE ( yes, thats right, another heartbeat file).
"""

import syslog
import time
import requests
import json
import ConfigParser
import heartbeat

MONITOR_CHECK_MK_HEARTBEAT_FILE = '/var/tmp/monitor_check_mk_heartbeat'
CHECK_MK_HEARTBEAT_FILE = '/var/tmp/check_mk_heartbeat'
HEARTBEAT_TIME_LIMIT = 600  # 10 minutes in seconds

config_file = '/etc/pagerduty.conf'


def pagerduty_api_key():
    """Get PagerDuty api key from a config file."""

    configParser = ConfigParser.ConfigParser()
    configParser.read(config_file)

    return configParser.get('pagerduty', 'api_key')


def generate_pagerduty_request_headers():
    """HTTP headers for a POST request to PagerDuty API."""

    return {
        'Authorization': "Token token=%s" % pagerduty_api_key(),
        'Content-Type': 'application/json',
        }


def generate_pagerduty_request_content():
    """Content of a POST request to PagerDuty API.
    service_key need to point to a preexisting pagerduty service."""

    return json.dumps({
        "service_key": "82031157a3b44d0b85bac794ee34ae2b",
        "event_type": "trigger",
        "description": "Check MK heartbeat file is STALE. Is Check_MK down?",
        "client": "checkmk-external.met.no",
        })


def trigger_incident():
    """Trigger PagerDuty by sending a POST to the PagerDuty API."""

    # Try to post incident twice before giving up.
    for _ in range(2):
        try:
            response = requests.post(
                'https://events.pagerduty.com/generic/2010-04-15/create_event.json',
                headers=generate_pagerduty_request_headers(),
                data=generate_pagerduty_request_content()
                )
            response.raise_for_status()
            return
        except:
            time.sleep(5)

    syslog.syslog(syslog.LOG_ERR,
                  "Could not reach pagerduty api to trigger incident!")
    raise


def monitor_checkmk_heartbeat():
    """Create and incident if the heartbeat time is too old."""

    heartbeatfile = heartbeat.HeartbeatFile(CHECK_MK_HEARTBEAT_FILE)
    if(not heartbeatfile.heartbeat_ok(HEARTBEAT_TIME_LIMIT)):
        trigger_incident()


if __name__ == '__main__':
    monitor_checkmk_heartbeat()

    heartbeatfile = heartbeat.HeartbeatFile(MONITOR_CHECK_MK_HEARTBEAT_FILE)
    heartbeatfile.register_heartbeat()
