# Makefile for Django project management
# Uses uv for dependency and virtual environment management
# Install uv: https://docs.astral.sh/uv/getting-started/

.PHONY: help install setup dev run seed migrate makemigrations createsuperuser shell test collectstatic db-up db-down db-reset docker-login-hub docker-login-ghcr

help:
	@echo "First time setup:"
	@echo "  make docker-login-hub   Log in to Docker Hub (postgres, maildev images)"
	@echo "  make docker-login-ghcr  Log in to ghcr.io (uv build image)"
	@echo "  make install            Install dependencies"
	@echo "  cp .env.example .env"
	@echo "  make setup              Start DB, migrate, and seed sample data"
	@echo "  make run                Start the dev server"
	@echo ""
	@echo "Daily use:"
	@echo "  dev              Start Docker services, migrate, then run the dev server"
	@echo "  run              Run the Django dev server (Docker already up)"
	@echo "  seed             Load sample admin user and test data"
	@echo "  migrate          Apply database migrations"
	@echo "  makemigrations   Create new migrations after model changes"
	@echo "  db-reset         Wipe and recreate the local database"
	@echo "  shell            Open the Django shell"
	@echo "  test             Run test suite"

docker-login-hub:
	docker login

docker-login-ghcr:
	@gh auth token | docker login ghcr.io -u $$(gh api user --jq '.login') --password-stdin

install:
	uv sync --all-extras

setup: db-up migrate seed
	@mkdir -p media
	@echo "Ready — run 'make run' to start the dev server"

dev: db-up migrate
	@mkdir -p media
	@-fuser -k 8000/tcp 2>/dev/null; true
	uv run python manage.py runserver

run:
	uv run python manage.py runserver

seed:
	uv run python manage.py seed

migrate:
	uv run python manage.py migrate

makemigrations:
	uv run python manage.py makemigrations

createsuperuser:
	uv run python manage.py createsuperuser

shell:
	uv run python manage.py shell

test:
	uv run python manage.py test

collectstatic:
	uv run python manage.py collectstatic --noinput

db-up:
	docker compose up -d db maildev
	@echo "Postgres is at localhost:$${POSTGRES_PORT:-5432}  maildev UI is at http://localhost:1080"

db-down:
	docker compose down

db-reset:
	docker compose down -v
	docker compose up -d db maildev
	@echo "Database wiped and recreated"
