# juice_task/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'juice_task.settings')
app = Celery('juice_task')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()