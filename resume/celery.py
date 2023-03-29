import os
from celery import Celery
import django
from django.conf import settings

# set the default Django settings module for the 'celery' program. Change `resume` with your project name.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume.settings')
django.setup()

# Change `resume` with your project name.
app = Celery('resume')

app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
