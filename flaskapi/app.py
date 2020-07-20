"""Initializing flask app and extensions"""
from json import JSONEncoder
from pathlib import Path, PurePath

import connexion
from flask import Flask

from flaskapi.extensions import celery, db, jwt, migrate


def create_app(test_config=None, cli=True):
    """Application factory, used to create application
    """
    app = Flask("__name__", instance_relative_config=True)
    app = connexion.FlaskApp(__name__, specification_dir="./")
    app.json_encoder = JSONEncoder

    # add connexion file to API
    app.add_api("openapi.yml")

    # sets path to instance config to relative to the instance folder.
    app.app.instance_relative_config = True

    app.app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:////"
        + str(PurePath(app.app.instance_path, "flaskapi.sqlite")),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_BLACKLIST_ENABLED=True,
        JWT_BLACKLIST_TOKEN_CHECKS=["access", "refresh"],
        CELERY_BROKER_URL="redis://localhost:6379/0",
        CELERY_RESULT_BACKEND="redis://localhost:6379/1",
    )

    try:
        Path(app.app.instance_path).mkdir(parents=True)
    except OSError:
        pass

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.app.config.from_mapping(test_config)

    configure_extensions(app.app, cli)
    init_celery(app.app)

    return app.app


def configure_extensions(app, cli):
    """configure flask extensions
    """
    db.init_app(app)
    jwt.init_app(app)

    if cli is True:
        migrate.init_app(app, db)


def init_celery(app=None):
    """Initialize Celery extension"""
    app = app or create_app()
    celery.conf.broker_url = app.config["CELERY_BROKER_URL"]
    celery.conf.result_backend = app.config["CELERY_RESULT_BACKEND"]
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
