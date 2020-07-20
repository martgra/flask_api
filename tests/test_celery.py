import pytest
import os

from flaskapi.app import init_celery
from flaskapi.tasks.example import dummy_task


@pytest.fixture
def celery_app(celery_app, app):
    os.environ.setdefault("FORKED_BY_MULTIPROCESSING", "1")

    celery = init_celery(app)
    celery_app.conf = celery.conf
    celery_app.Task = celery_app.Task
    celery_app.conf["task_always_eager"] = True
    yield celery_app


@pytest.fixture(scope="session")
def celery_worker_pool():
    return "prefork"


def test_example(celery_app, celery_worker_pool):
    """Simply test our dummy task using celery"""
    print("HERE")
    res = dummy_task.delay()
    assert res.get() == "OK"
