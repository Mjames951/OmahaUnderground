# Makefile for Django project management
# Uses uv for dependency and virtual environment management
# Install uv: https://docs.astral.sh/uv/getting-started/

.PHONY: help install run migrate makemigrations createsuperuser shell test collectstatic

help:
	@echo "Commonly used make targets:"
	@echo "  install          Install dependencies with uv"
	@echo "  run        Run the Django development server"
	@echo "  migrate          Apply database migrations"
	@echo "  makemigrations   Create new database migrations"
	@echo "  createsuperuser  Create a new Django superuser"
	@echo "  shell            Open the Django shell"
	@echo "  test             Run Django tests"
	@echo "  collectstatic    Collect static files"

install:
	uv sync --all-extras

run:
	uv run python manage.py runserver

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
