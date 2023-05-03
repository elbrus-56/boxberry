from config.celery import app
from orders.services import orders


@app.task
def check_status_delivery_order_task():
    task = orders.OrdersServices()
    return task.check_status_delivery_order()


app.autodiscover_tasks()
