import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")


app.conf.beat_schedule = {
    "check_status_delivery_order_task": {
        "task": "orders.task.check_status_delivery_order_task",
        "schedule": crontab(
            minute="0", hour="*"
        ),
    }
}
