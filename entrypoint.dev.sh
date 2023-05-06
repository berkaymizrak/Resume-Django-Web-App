#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while [ "$(pg_isready -h $SQL_HOST -p $SQL_PORT)" != "$SQL_HOST:$SQL_PORT - accepting connections" ]; do
      sleep 1
    done

    echo "PostgreSQL started"
fi

if [ "$SERVICE_NAME" = "app_resume" ]; then

  echo " --- --- --- --- --- --- --- --- --- "
  echo "Creating database migrations"
  python manage.py makemigrations

  echo " --- --- --- --- --- --- --- --- --- "
  echo "Applying database migrations"
  python manage.py migrate --noinput

  echo " --- --- --- --- --- --- --- --- --- "
  echo "Flushing database"
  #python manage.py flush --no-input

  #	python manage.py collectstatic --noinput

  echo " --- --- --- --- --- --- --- --- --- "
  echo "Creating default superuser"
  python manage.py createsuperuser --username="$DJANGO_SUPER_USERNAME" --email="$DJANGO_SUPER_USER_EMAIL" --no-input

fi

echo " --- --- --- --- --- --- --- --- --- "
echo "Starting server"
exec "$@"

# To make migrations in continuous development, RUN:
# docker exec -it app_resume python manage.py makemigrations
# docker exec -it app_resume python manage.py migrate

# Update requirements after adding new packages:
# docker exec -it app_resume pip freeze > requirements.txt

# Clear models:
# docker exec -it app_resume python manage.py clear_models
