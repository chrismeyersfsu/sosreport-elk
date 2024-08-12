Given an SOSReport tar.gz, extract it, feed the logs into loki and view them in Grafana.
Given an OTEL zstd compressed log from awx, replay it into loki and view it in Grafana.

### Quickstart

```
docker compose up
cp <your_sos_report.tar.xv> ./sosreport/
OR
cp awx-logs.json.zstd ./logs2replay/
```
* Load Grafana to see the results http://localhost:3002

### Importing Dashboards

A dashboard exists in source control as a json. You currently need to manually import it. Ideally, it will auto-import.

