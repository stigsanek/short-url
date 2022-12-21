run:
	poetry run python manage.py runserver

locale:
	poetry run python manage.py makemessages -l en
	poetry run python manage.py compilemessages

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

createsuperuser:
	poetry run python manage.py createsuperuser

install:
	poetry install

lint:
	poetry run flake8 short_url

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=short_url --cov-report xml
