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
