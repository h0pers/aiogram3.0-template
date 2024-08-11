include .env

bot-bash:
	docker exec -it aiogram30-template-bot-1 bash

db-bash:
	docker exec -it aiogram30-template-db-1 bash

makemigrations:
	alembic revision --autogenerate

migrate:
	alembic upgrade head

run:
	docker compose up -d --build --force-recreate

test:
	pytest -s

logs:
	docker compose logs -f

stop:
	docker compose down --remove-orphans

