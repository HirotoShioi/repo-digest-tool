.PHONY: build run-dev run down logs shell clean init-db frontend

build:
	docker compose build

run-dev:
	make init-db
	docker compose up --watch api

frontend:
	pushd frontend && npm run dev && popd

run:
	make init-db
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

shell:
	docker compose exec api bash

clean:
	docker compose down --remove-orphans -v


init-db:
	touch repo_tool.db

	