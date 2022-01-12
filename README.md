# Resume

## About

The project is set on Docker for development server and set configurations for Heroku for production server.

Django is used for backend, Postgres is used for database. Also Celery can be implemented easily.

## Installation

To start project,

1. First create a docker.env file from env.txt. Change&enter required parameters.


2. Start postgres at background:

    `docker-compose up -d --build postgres_resume`


3. Start app on terminal and track errors, to make continuous development:

   `docker-compose up --build app_resume`

## Django Management Command

A Django management command is created as colorful with user-friendly progressbar and the functionality is just for example.

To run:

   `docker-compose exec app_resume python manage.py clear_models`

![Django Command Screenshot](https://github.com/berkaymizrak/Resume-Django-Web-App/blob/main/screenshot_command.png?raw=true)

