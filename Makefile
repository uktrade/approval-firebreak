
makemigrations:
	docker-compose run --rm approval python manage.py makemigrations

migrations:
	docker-compose run --rm approval python manage.py makemigrations

migrate:
	docker-compose run --rm approval python manage.py migrate

shell:
	docker-compose run --rm approval python manage.py shell

bash:
	docker-compose run --rm approval bash

up:
	docker-compose up

down:
	docker-compose down

build:
	docker-compose build

all-requirements:
	docker-compose run --rm approval pip-compile --output-file requirements/base.txt requirements.in/base.in
	docker-compose run --rm approval pip-compile --output-file requirements/dev.txt requirements.in/dev.in
	docker-compose run --rm approval pip-compile --output-file requirements/prod.txt requirements.in/prod.in
