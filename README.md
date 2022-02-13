# Resume

## About

The project is set on Docker for development server and set configurations for Heroku and AWS S3 for production server.

Django is used for backend, Postgres is used for database. Also Celery can be implemented easily.

Some features:

* Django Management Command


* **Docker** for continuous development server


* Demo data comes with *"migrate"*. RunPython command is set for demo data.


* **/\<slug>/** : (_views.special_links_) Any first level of path in the url are checked first in 'Document' and then 'ImageSettings'. If path matches with 'name' field, it redirects to document(media) url or if it is an ImageSettings object returns the image page within max screen size image(javascript makes it) with layout of page(all meta and head).


* 404, 403, 500 pages are set.


* **CanonicalMiddleware:** if you use Heroku, this middleware redirects requests from herokuapp.com to your domain.


* **ParameterMiddleware:** receive people who come with reference of other users with get parameter of 'ref'
    and saves it into the session. Thus, if user visit other pages of website, all get parameters and 'ref' will stay
    end of the url all the time, on all different links.


* **custom_storage:** There are 3 type of storages in purpose. Uploaded documents, images(from ImageSettings model) and all other media are uploads different locations. 3 type of storage managements are set for development and production separately.


* **template_filters:** has several functions to manage parameters in html templates.


* Heroku and Amazon S3 integrations are ready.

## Installation

To start project,

1. First create a docker.env file from env.txt. Change&enter required parameters.


2. Start services at background:

    `docker-compose up -d --build`


3. Follow outputs alive and track errors, to make continuous development:

   `docker logs --follow app_resume`

Default admin account will be:

username: admin

password: 123456@@

## Production

Usage on Heroku:

1. Make integrations with Heroku and AWS S3.

2. After login to Heroku with help of Heroku CLI, push code to Heroku.

3. *"Reveal Config Vars"* on Heroku dashboard, check env.txt for parameters.

4. Run:

       heroku run python manage.py migrate
       heroku run python manage.py collectstatic --noinput
       heroku run python manage.py createsuperuser

## Django Management Command

A Django management command is created as colorful with user-friendly progressbar and the functionality is just for example.

To run:

   `docker-compose exec app_resume python manage.py clear_models`

![Django Command Screenshot](https://github.com/berkaymizrak/Resume-Django-Web-App/blob/main/screenshot_command.png?raw=true)


