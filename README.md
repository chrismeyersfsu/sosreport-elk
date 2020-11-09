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

Dashboards that are useful for SOSReport data are saved in `kibana_saved_objects`
in this repository. To import them into kibana follow the steps below:
* Open you kibana dashboard at http://localhost:5601
* Navigate to `Stack Management -> Saved objects`
* Click import
* Drag and drop or select the dashboards from the `kibana_saved_objects` directory
* Click Import

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

### Use-Case, NGINX 500s

From a failing nightly run in our jenkins server, I downloaded and extracted 
an SOSReport. I went to the `[Filebeat Nginx] Access and error logs ECS`
dashboard that is autoloaded into Kibana by `filebeat setup` that is run behind
the scenes one of the `docker-compose` containers via the init script `filebeat.sh`. 
I then searched for all 500 nginx errors `http.response.status_code:500`. Below 
is a screenshot of those results.

![nginx 500 list](../assets/kibana_nginx_500.png?raw=true)

Now, that is not much detail. So I head over to the tower logs for more detail
on this organization `/api/v2/organizations/2649/`. I enter the query 
`event.module:tower and message:"/api/v2/organizations/2649/"`. Below is a screenshot
of the results
![tower correlated 500](../assets/kibana_tower_500.png?raw=true)

Bingo, this random SOSReport has an elusive deadlock Traceback found. Oh man,
deadlocks are notoriously hard to debug. There are at least two sides to a deadlock.
I've found 1 side, the DELETE to organization 2649. What is on the other side and
what integration test(s) are running? Note the time the deadlock happens and look
at all events happening during that time.

### Debugging

*I don't see any logs in Kibana*
Check your time window. The default is "Last 15 Minutes". I usually set it to "Last 1 Year"

*I checked my time window and I still don't see logs in Kibana*
The `filebeat run` command that sends data to elasticsearch may have failed. Run `docker logs sosreport-elk_filebeat_1` and report the error.
A "normal" looking successfull log looks like the below.

```
Overwriting ILM policy is disabled. Set `setup.ilm.overwrite: true` for enabling.

Index setup finished.
Loading dashboards (Kibana must be running and reachable)
Loaded dashboards
Setting up ML using setup --machine-learning is going to be removed in 8.0.0. Please use the ML app instead.
See more: https://www.elastic.co/guide/en/machine-learning/current/index.html
Loaded machine learning job configurations
Loaded Ingest pipelines
```

*Something went sideways.*
Delete the existing ELK stack and start over via `docker-compose up --force-recreate`
