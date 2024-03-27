from celery import Celery
from datetime import timedelta
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django-shop.settings')  # setting for celery

celery_app = Celery('django-shop')   # create instance of celery

celery_app.autodiscover_tasks()   # run tasks automatically


celery_app.conf.broker_url = 'amqp://'   # Celery broker
celery_app.conf.result_backend = 'rpc://'  # Celery result backend
celery_app.conf.task_serializer = 'json'   # task serializer to JSON
celery_app.conf.result_serializer = 'pickle'  # result serializer to pickle
celery_app.conf.accept_content = ['json', 'pickle']   # accepted content types for tasks and results
celery_app.conf.result_expires = timedelta(days=1)  # expiration time
celery_app.conf.task_always_eager = False   # Disabling eager execution of tasks
celery_app.conf.worker_prefetch_multiplier = 4   # worker prefetch multiplier
