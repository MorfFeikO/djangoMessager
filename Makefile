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
init-start: db-init migrate superuser runserver
	@echo 'Server successfuly started.'


