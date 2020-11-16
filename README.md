Push SOSReport logs into an ELK stack running locally via docker-compose.

Current log files processed:
* /var/log/tower/*.log
* /var/log/nginx/access.log
* /var/log/nginx/error.log

### Quickstart

* Download and extract an SOSReport
* Run the below commands to start the ELK stack and ingest the SOSReport
```
ansible-playbook main.yml -v -e sosreports_dir=/home/meyers/Downloads/sos/all_tower_sos_reports
docker-compose up
```
* Load Kibana to see the results http://localhost:5601

### Screenshot
Below is a view of Kibana Discover after the data has been loaded. The filter
`event.module:tower` has been applied to limit the results to only log entries
that were processed by the `filebeat` `tower` module.

![kibana discover tower](../assets/kibana_tower_discover.png?raw=true)


### Importing Dashboards

Dashboards are now auto-imported.

### Contribute Useful Dashboard

At this point, you have successfully loaded an SOSReport into the ELK stack, have
played around with it, have seen the value, and have even created your own visualization
that you think others would find helpful. Now you want to contribute your useful
dashboard.

* Save your discover view / dashboard / visualization
* Head over to `Stack Management -> Saved objects` and find your entry
* Check your entry and click the Export button
* Turn off `Include related objects` and click Export
* Download the file to the `kibana_saved_objects/` in this repository
* Submit a PR !!

### Debugging

*I don't see any logs in Kibana*</br>
The ELK stack takes about 2 minutes to come up and begin processing. If you think
the processing should be finished but still don't see results check your time window. 
The default is "Last 15 Minutes". I usually set it to "Last 1 Year"

*I checked my time window and I still don't see logs in Kibana*</br>
The `filebeat run` command that sends data to elasticsearch may have failed. Run `docker logs sosreport-elk_filebeat_1` and report the error.
A "normal" looking successfull log looks like the below.

```
Loaded Ingest pipelines
Loading dashboards (Kibana must be running and reachable)
Loaded dashboards
```

*Something went sideways.*</br>
Delete the existing ELK stack and start over via `docker-compose up --force-recreate`

*It looks like nothing is happening*</br>
It can take some time to import an SOSReport and show up in the Kibana dashboard. Although you can't see a percentage view or anything that tells you how far filebeat is from completion, you can see a historical processing view in kibana. Go to `Stack Monitoring` from the hamburger menu on the left. Below is an example of the view that you should see. From this view, you can see the rate at which filebeat events are being processed as well as the total number of events processed so far.

![filebeat metrics](../assets/debug_elasticsearch_filebeat_metrics.png?raw=true)
