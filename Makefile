
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
	docker-compose run --rm approval python manage.py create_test_user --email=hiring-manager@mail.ci.uktrade.digital --group="Hiring Managers" --password=password --first_name=Ian --last_name=HiringManager
	docker-compose run --rm approval python manage.py create_test_user --email=chief@mail.ci.uktrade.digital --group="Chiefs" --password=password --first_name=Clement --last_name=Chief
	docker-compose run --rm approval python manage.py create_test_user --email=busop@mail.ci.uktrade.digital --group="Business Operations" --password=password --first_name=Billy --last_name=BusOps
	docker-compose run --rm approval python manage.py create_test_user --email=hr@mail.ci.uktrade.digital --group="HR" --password=password --first_name=John --last_name=Hr
	docker-compose run --rm approval python manage.py create_test_user --email=finance@mail.ci.uktrade.digital --group="Finance" --password=password --first_name=Jane --last_name=Finance
	docker-compose run --rm approval python manage.py create_test_user --email=commercial@mail.ci.uktrade.digital --group="Commercial" --password=password --first_name=Bob --last_name=Commercial

superuser:
	docker-compose run --rm approval python manage.py createsuperuser
