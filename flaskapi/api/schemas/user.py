"""Database Schema for the User"""
from flaskapi.models import User
from flaskapi.extensions import ma, db

class UserSchema(ma.SQLAlchemyAutoSchema):
    """UserSchema Class"""

    id = ma.Int(dump_only=True)
    password = ma.String(load_only=True, required=True)

    class Meta:
        """TODO: Unknown class"""
        model = User
        sqla_session = db.session
        load_instance = True
