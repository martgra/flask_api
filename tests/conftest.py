import json
import tempfile
import os
from pathlib import PurePath

import pytest
from dotenv import load_dotenv
from pytest_factoryboy import register

from flaskapi.app import create_app
from flaskapi.extensions import db as _db
from flaskapi.models import User
from tests.factories import UserFactory

load_dotenv('.flaskenv')

register(UserFactory)

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(test_config={
        "TESTING": True, 
        "SQLALCHEMY_DATABASE_URI": "sqlite:////" + db_path})
    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        print(app.config["SQLALCHEMY_DATABASE_URI"])
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def admin_user(db):
    user = User(
        username='admin',
        email='admin@admin.com',
        password='admin'
    )

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def admin_headers(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['access_token']
    }


@pytest.fixture
def admin_refresh_headers(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['refresh_token']
    }