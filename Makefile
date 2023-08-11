all:
	ansible-playbook main.yml

test: FORCE
	docker-compose -f docker-compose.yaml -f test/directory_watch_sosreport/docker-compose.yaml up

FORCE: ;
