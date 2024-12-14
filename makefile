.PHONY: build run-dev run down logs shell clean

build:
	docker compose build

run-dev:
	docker compose up --watch api

run:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

shell:
	docker compose exec api bash

clean:
	docker compose down --remove-orphans -v