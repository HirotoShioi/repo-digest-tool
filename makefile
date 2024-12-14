.PHONY: build run run-dev down logs shell clean

build:
	docker compose build

run-dev:
	docker compose up --watch api

run:
	docker compose --profile frontend up --watch

down:
	docker compose down

logs:
	docker compose logs -f

shell:
	docker compose exec api bash

clean:
	docker compose down -v