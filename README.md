Push SOSReport logs into an ELK stack running locally via docker-compose.

Current log files processed:
* /var/log/tower/*.log
* /var/log/nginx/access.log
* /var/log/nginx/error.log

```
ansible-playbook main.yml -v -e sosreports_dir=/home/meyers/Downloads/sos/all_tower_sos_reports
docker-compose up
```
http://localhost:5601

![Demo Animation](../assets/kibana_nginx_500.png?raw=true)
