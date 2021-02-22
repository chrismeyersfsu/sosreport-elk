#!/bin/bash
# Remove all dashboards that ship with the container except the nginx one, it's useful
# Also, our custom dashboards will NOT be deleted in this process because we map them read only
find kibana/7/dashboard/ -type f -not -name '*nginx*' -delete || true

while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' elk:9200)" != "200" ]]; do sleep 1; done
while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' elk:5601/app/home/)" != "200" ]]; do sleep 1; done
filebeat --strict.perms=false setup --pipelines
filebeat --strict.perms=false setup --dashboards
#filebeat --strict.perms=false -e -d "*" run
filebeat --strict.perms=false run
echo "Successfully processed log files, exiting now!"
