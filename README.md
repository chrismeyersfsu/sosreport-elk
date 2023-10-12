Push SOSReport logs into an Loki running locally via docker-compose and query via Grafana.

Current log files processed:
* /var/log/nginx/access.log

### Quickstart

```
docker-compose up
cp <your_sos_report.tar.xv> ./sosreport/
```
* Load Grafana to see the results http://localhost:3001

### Importing Dashboards

A dashboard exists in source control as a json. You currently need to manually import it. Ideally, it will auto-import.

