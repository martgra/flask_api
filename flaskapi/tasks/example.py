"""Example of Celery tasks"""
from flaskapi.extensions import celery


@celery.task
def dummy_task():
    """Dummy task to test celery"""
    return "OK"
