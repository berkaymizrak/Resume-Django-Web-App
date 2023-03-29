import os
from celery import Celery
import django

# set the default Django settings module for the 'celery' program. Change `resume` with your project name.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume.settings')
django.setup()

# Change `resume` with your project name.
app = Celery('resume')

app.config_from_object('django.conf:settings')


# Load task modules from all registered Django app configs.

# if you are using app names directly, you can use this: (user)
# from django.conf import settings
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# or if you are using app names as dotted paths, you can use this: (user.apps.UserConfig)
# from django.apps import apps
# app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

# if you are using Celery 4.x you can use:
app.autodiscover_tasks()

