# Celery worker definition
from celery import Celery

celery_app = Celery('sync_worker', broker='redis://localhost:6379/0')

@celery_app.task
def run_sync():
    pass
