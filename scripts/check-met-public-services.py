#!/usr/bin/python

import requests
import re
import os
import syslog

HEARTBEAT_FILE = '/var/lib/check_mk_heartbeat'
NAGIOS_STATUS = {
    'OK': 0,
    'WARN': 1,
    'CRIT': 2,
    'UNKNOWN': 3
}

services = {
    'public-wms': {
        'url': 'http://public-wms.met.no'
        },
    'api.met.no': {
        'url': 'http://api.met.no',
        'regex_content': 'Velkommen\stil\sapi\.'
        },
    'halo.met.no': {
        'url': 'https://halo.met.no'
        },
    'bw-wms.met.no': {
        'url': 'http://bw-wms.met.no'
        },
    'thredds.met.no': {
        'url': 'http://thredds.met.no'
        },
    'spesial.met.no': {
        'url': 'http://spesial.met.no'
        }

    }


def check_all_services():
    """Run a check for all services and print output in check_mk local_check
       format."""

    for service in services:
        status, msg = check_service(services[service]['url'],
                                    services[service].get('regex_content', None))

        print "%s Service_%s - %s - %s" % (NAGIOS_STATUS[status], service,
                                           status, msg)


def check_service(url, regex_content=None):
    """Check http service url and return status and text."""
    try:
        req = requests.get(url, timeout=1.0)
        req.raise_for_status()
    except requests.exceptions.ConnectionError:
        return 'CRIT', 'Connection refused.'
    except requests.exceptions.Timeout:
        return 'WARN', 'Request timed out.'
    except requests.exceptions.HTTPError:
        return 'CRIT', "Got bad status code from service: %s" % req.status_code
    except:
        return 'UNKNOWN', "Service check returned unknown exception! Service status code: %s" % (req.status_code if req.status_code else "Missing!")

    if regex_content is not None:
        if re.search(regex_content, req.content) is None:
            return 'CRIT', "Missing content in response. Service status code: %s" % req.status_code

    return 'OK', "All is well. Service status code: %s" % req.status_code


def register_check_mk_heartbeat():
    """Touch heartbeat file each time this local_check is called to signal that
       check_mk is alive...Its alive Dr. Frankenstein!"""
    try:
        with open(HEARTBEAT_FILE, 'a'):
            os.utime(HEARTBEAT_FILE, None)
    except IOError:
        syslog.syslog(syslog.LOG_ERR, "Could not update heartbeat file %s." %
                      HEARTBEAT_FILE)


if __name__ == "__main__":
    register_check_mk_heartbeat()
    check_all_services()
