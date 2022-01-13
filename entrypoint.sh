#!/bin/bash
if [ "$COMMANDS" = "1" ]; then
	python manage.py migrate --noinput
#	python manage.py collectstatic --noinput
	python manage.py createsuperuser --username="$DJANGO_SUPER_USERNAME" --email="$DJANGO_SUPER_USER_EMAIL" --no-input
fi
python manage.py runserver 0.0.0.0:8001

# To make migrations in continues development, RUN:
# docker-compose exec app_resume python manage.py makemigrations
# docker-compose exec app_resume python manage.py migrate
