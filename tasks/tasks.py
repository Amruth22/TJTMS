# tasks/tasks.py
from celery import shared_task

@shared_task
def test_task(message):
    print(f"Task executed: {message}")
    return message
    