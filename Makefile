migrate-init:
	python manage.py migrate
makemigrations:
	python manage.py makemigrations
migrate: makemigrations migrate-init
	@echo 'Made migration!'
superuser:
	python manage.py createsuperuser
runserver:
	python manage.py runserver
coverage:
	coverage run --source='.' manage.py test
report:
	coverage report -m
db-init:
	sudo -u postgres createdb newdb2;
init-start: venv init-poetry db-init migrate superuser runserver
	@echo 'Server successfuly started.'
init-poetry:
	curl -sSL https://install.python-poetry.org | python3 -
venv:
	python3 -m venv venv

