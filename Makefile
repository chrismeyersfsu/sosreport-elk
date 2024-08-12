all:
	docker compose up

test: FORCE
	docker compose -f docker-compose.yaml -f test/directory_watch_sosreport/docker-compose.yaml up

FORCE: ;

clean:
	rm -rf volumes/loki/index/* volumes/loki/boltdb-cache/*
	rm -rf volumes/promtail/position_data/*
