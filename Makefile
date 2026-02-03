# Makefile for Django project management

.PHONY: help runserver migrate makemigrations createsuperuser shell test collectstatic

help:
	@echo "Commonly used make targets:"
	@echo "  runserver        Run the Django development server"
	@echo "  migrate          Apply database migrations"
	@echo "  makemigrations   Create new database migrations"
	@echo "  createsuperuser  Create a new Django superuser"
	@echo "  shell            Open the Django shell"
	@echo "  test             Run Django tests"
	@echo "  collectstatic    Collect static files"

runserver:
	. venv/bin/activate && python manage.py runserver

migrate:
	. venv/bin/activate && python manage.py migrate

makemigrations:
	. venv/bin/activate && python manage.py makemigrations

createsuperuser:
	. venv/bin/activate && python manage.py createsuperuser

shell:
	. venv/bin/activate && python manage.py shell

test:
	. venv/bin/activate && python manage.py test

collectstatic:
	. venv/bin/activate && python manage.py collectstatic --noinput
