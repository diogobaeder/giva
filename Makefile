build: test

test:
	DJANGO_SETTINGS_MODULE=test_settings python manage.py test

run:
	python manage.py runserver

freeze-requirements:
	pip freeze | grep -v memcache > requirements.txt
