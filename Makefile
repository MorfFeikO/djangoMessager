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

