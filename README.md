# Tools for monitoring MET public services and check_mk

## Installation
```
apt-get install git
cd /usr/local/share
git clone git@gitlab.met.no:it-geo/check-met-public-services.git
apt-get install check-mk-agent
apt-get install xinetd

cd /usr/lib/check_mk_agent/local/ 
ln -s /usr/local/share/check-met-public-services/scripts/check-met-public-services.py
ln -s /usr/local/share/check-met-public-services/scripts/check-monitor_check_mk.py
cd /usr/local/bin/
ln -s <path_to_repo/scripts/monitor_check_mk.py
```

Add monitor_check_mk to cron.d:
```
*/10   *    *   *   *  nobody  /usr/local/bin/monitor_check_mk.py > /dev/null
```

Edit 'only_from' and 'disable' directive in /etc/xinetd.d/check_mk and restart service:
```
restart xinetd
```

Create a fresh PagerDuty API key and stick in /etc/pagerduty.conf, like so:
```
[pagerduty]
api_key = '<key_here>'
```

Do inventory on Check_mk server and the checks should show up.