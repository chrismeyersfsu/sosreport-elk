#!/bin/bash
find kibana/7/dashboard/ -type f -not -name '*nginx*' -not -name '*tower*' -delete

while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' elk:9200)" != "200" ]]; do sleep 1; done
while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' elk:5601/app/home/)" != "200" ]]; do sleep 1; done
filebeat --strict.perms=false setup --pipelines
filebeat --strict.perms=false setup --dashboards
filebeat --strict.perms=false run
echo "Successfully processed log files, exiting now!"
