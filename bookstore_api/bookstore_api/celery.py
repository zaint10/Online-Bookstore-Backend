# celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore_api.settings')

app = Celery('bookstore_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
