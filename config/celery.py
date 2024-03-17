import os

from celery import Celery

from config.settings import CLOUDAMQP_URL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('proj', backend='rpc://', broker=CLOUDAMQP_URL)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
