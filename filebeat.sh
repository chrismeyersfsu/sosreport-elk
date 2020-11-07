#!/bin/bash
while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' elk:9200)" != "200" ]]; do sleep 1; done
while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' elk:5601/app/home/)" != "200" ]]; do sleep 1; done
filebeat setup
filebeat run
