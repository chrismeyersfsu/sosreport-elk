Push NGINX logs into elasticsearch from 1 or many sosreports. Run the `ansible-playbook` command below to generate a `docker-compose.yml` file. Then, `docker-compose up` to bring up an ELK stack and a `filebeat` container that will push the sosreport data into the ELK stack.

```
ansible-playbook main.yml -v -e sosreports_dir=/home/meyers/Downloads/sos/all_tower_sos_reports
docker-compose up
```
http://localhost:5601
