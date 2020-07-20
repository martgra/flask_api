"""API routes for User"""
from flask import request
from sqlalchemy.exc import IntegrityError

from flaskapi.api.schemas import UserSchema
from flaskapi.extensions import db
from flaskapi.models import User


def get_secret(user) -> str:
    """Example of method that needs authorization"""
    return "You are {user} and the secret is 'wbevuec'".format(user=user)


def get_user(user_id) -> str:
    """Get a specific user"""
    schema = UserSchema()
    user = User.query.get_or_404(user_id)
    return {"user": schema.dump(user)}


def create_user(body):
    """Create a specific user"""
    print(body)
    data = request.json
    schema = UserSchema()
    user = schema.load(data)
    try:
        db.session.add(user)
        db.session.commit()
        return {"message": "user created", "user": schema.dump(user)}, 201
    except IntegrityError as error:
        # If UNIQUE constraint is violated - return message pointing to conflict
        return {"message": "{} already exist".format(str(error.orig).split(".")[1])}, 409


def get_users():
    """Return a list of all users"""
    schema = UserSchema(many=True)
    query = User.query
    return {"message": "List of users", "users": schema.dump(query)}


def update_user(body, user_id=None):
    """Update specific user"""
    schema = UserSchema(partial=True)
    user = User.query.get_or_404(user_id)
    user = schema.load(body, instance=user)
    db.session.commit()
    return {"message": "user updated", "user": schema.dump(user)}


def delete_user(user_id):
    """Delete specific user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return {"message": "user deleted"}
