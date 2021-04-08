
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

test-users:
	docker-compose run --rm approval python manage.py create_test_user --password=password --first_name=John --last_name=Submitter --is_admin=True
	docker-compose run --rm approval python manage.py create_test_user --email=hiring-manager@test.com --group="Hiring Managers" --password=password --first_name=Hiring --last_name=Manager
	docker-compose run --rm approval python manage.py create_test_user --email=chief@test.com --group="Chiefs" --password=password --first_name=Chief --last_name=Chief
	docker-compose run --rm approval python manage.py create_test_user --email=busop@test.com --group="Business Operations" --password=password --first_name=Business --last_name=Ops
