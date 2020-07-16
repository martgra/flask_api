from functools import partial
from flaskapi.api.schemas import UserSchema
from flaskapi.models import User
from flaskapi.extensions import db
from flask import request
from flaskapi.commons.pagination import paginate


def get_secret(user) -> str:
    return "You are {user} and the secret is 'wbevuec'".format(user=user)


def get_user(user_id) -> str:
    schema = UserSchema()
    user = User.query.get_or_404(user_id)
    return {"user": schema.dump(user)}


def create_user(body):
    print(body)
    data = request.json
    schema = UserSchema()
    user = schema.load(data)

    db.session.add(user)
    db.session.commit()

    return {"msg": "user created", "user": schema.dump(user)}, 201


def get_users():
    schema = UserSchema(many=True)
    query = User.query
    return schema.dump(query)


def update_user(body, user_id=None):
    schema = UserSchema(partial=True)
    user = User.query.get_or_404(user_id)
    user = schema.load(request.json, instance=user)
    db.session.commit()
    return {"msg": "user updated", "user": schema.dump(user)}


def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()