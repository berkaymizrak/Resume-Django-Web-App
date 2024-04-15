# Resume

## About

The project is set on Docker for development server and set configurations for Heroku and AWS S3 for production server.

Django is used for backend, Postgres is used for database. Also Celery can be implemented easily.

Some features:

* Django Management Command


* **Docker** for continuous development server


* Demo data comes with *"migrate"*. RunPython command is set for demo data.


* **/\<slug>/** : (_views.special_links_) Any first level of path in the url are checked first in 'Document'
  and then 'ImageSettings'. If path matches with 'name' field, it redirects to document(media) url or
  if it is an ImageSettings object returns the image page within max screen size image(javascript makes it)
  with layout of page(all meta and head).


* 404, 403, 500 pages are set.


* **CanonicalMiddleware:** if you use Heroku, this middleware redirects requests from herokuapp.com to your domain.


* **ParameterMiddleware:** receive people who come with reference of other users with get parameter of 'ref'
  and saves it into the session. Thus, if user visit other pages of website, all get parameters and 'ref' will stay
  end of the url all the time, on all different links.


* **custom_storage:** There are 3 type of storages in purpose. Uploaded documents, images(from ImageSettings model) and
  all other media are uploads different locations. 3 type of storage managements are set for development and production
  separately.


* **template_filters:** has several functions to manage parameters in html templates.


* Heroku and Amazon S3 integrations are ready.

## Installation

To start project,

1. First create a docker.env file from env.txt. Change&enter required parameters.


2. Start services at background:

   `docker-compose up --build -d`


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

``` bash
heroku run python manage.py migrate
heroku run python manage.py collectstatic --noinput
heroku run python manage.py createsuperuser

docker exec -it app_resume python manage.py migrate
docker exec -it app_resume python manage.py makemigrations
docker exec -it app_resume pip freeze > requirements.txt

 ```

## Setting a Cron Job

### Overview

This is going to be a quickstart for the new users for cron job.
I am not using cron job actively in this project,
but you can still find a few files for cron job in the project, and I am explaining them here.
This doc also contains some examples of cron job and mailqueue package which is scheduling sending mails to not be spam.

At the end of this doc, you will find `PERIODIC TASKS` section in admin panel.
In the panel you will be able to set cron job for each task.
A useful link to set correct frequency for each job: [https://crontab.guru/](https://crontab.guru/)

### Install Requirements

This part will explain how to set up cron jobs on celery for especially Heroku integration.
This can be still used for any other production integration too.
Since the cron job is not installed on this project,
you will not get the requirements for cron job from requirements.txt.
Therefore, you will need to install some requirements as below but the rest settings are done in the code files,
so you can grab and use everything.
(Below installation will install redis, celery and django-celery-beat packages.)

``` bash
 pip install -r requirements_celery.txt
 ```

* To use cron jobs we need first celery.
  Celery beat is a scheduler; It kicks off tasks at regular intervals, that are then executed by available worker nodes
  in the cluster. [[Celery Doc](https://docs.celeryq.dev/en/master/userguide/periodic-tasks.html)]

* And we need redis to store the cron jobs on Heroku.

Additionally, I offer to install mailqueue package for scheduling sending mails to not be spam.

``` bash
 pip install django-mail-queue
 ```

### Code Preparation

1. **Settings.py**

Add the following line to settings.py file:

``` python
INSTALLED_APPS = [
    ...
    'django_celery_beat',
]
```

Comment out the lines between `CELERY` hashtag. The settings are set in here for Heroku.
You can check the celery documentation for more details.

2. **__init__.py**

Add the following line to `__init__.py` file that is in the same directory as `settings.py` file:

``` python
from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
```

3. **celery.py**

There is a `celery.py` file has been already created in this project in the same directory as `settings.py` file.
This is needed to set up the celery app.

4. **tasks.py**

There is a `tasks.py` file has been already created in this project in the user folder which is an app in this project.
This is where we set the cron jobs. This file can be created in any other app.

5. **Procfile**

Add the following line to `Procfile` file:

``` bash
main_worker: celery -A user worker -B -l INFO --without-gossip --without-mingle --without-heartbeat
```

This will help Heroku to recognize the celery app. This will work as separate dyno in Heroku.

### Use Cases

You can find several functions in the `tasks.py` file, and they can be scheduled from admin panel as mentioned above.
Each function is described in itself enough to understand.
I would like to add an example for send_mail_queued function.
You can use this code snippet in any `view.py` file.

``` python
from core.tasks import send_mail_queued
from django.conf import settings
...
def contact_page(request):
    ...
    send_mail_queued.delay(
        mail_subject=form.cleaned_data['subject'],
        message_context=form.cleaned_data['message'],
        to=settings.DEFAULT_FROM_EMAIL,
        reply_to=form.cleaned_data['email'],
    )

    return ...
```

`.delay()` is an API for celery. It is used to schedule the task.

## Django Management Commands

* Just to remind, session flushing command can be run periodically if the django_session table became huge.

* * Locally:

  `docker-compose exec app_resume python manage.py clearsessions`

* * In Heroku Production:

  `heroku run python manage.py clearsessions`


* Additionally, a Django management command is created as colorful with user-friendly progressbar and the functionality
  is just to be an example. Running:

  `docker-compose exec app_resume python manage.py clear_models`

![Django Command Screenshot](https://github.com/berkaymizrak/Resume-Django-Web-App/blob/main/screenshot_command.png?raw=true)


