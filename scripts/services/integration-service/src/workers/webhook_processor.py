from celery import Celery

celery_app = Celery('webhook_processor', broker='redis://localhost:6379/0')

@celery_app.task
def process_webhook(payload):
    pass
