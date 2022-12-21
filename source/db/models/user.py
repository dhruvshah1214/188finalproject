# server/models/user.py


import jwt
import datetime
import os

from source.db import bcrypt

import sqlalchemy as sqa
import sqlalchemy.orm as orm
from source.db import Model

from source.db.models.monitor import Monitor


class User(Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = sqa.Column(sqa.Integer, primary_key=True, autoincrement=True)
    email = sqa.Column(sqa.String(255), unique=True, nullable=False)
    password = sqa.Column(sqa.String(255), nullable=False)
    created = sqa.Column(sqa.DateTime, nullable=False)
    admin = sqa.Column(sqa.Boolean, nullable=False, default=False)
    monitors = orm.relationship("Monitor", order_by=Monitor.id, back_populates="user")

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password, int(os.environ.get('BCRYPT_LOG_ROUNDS'))).decode()
        self.created = datetime.datetime.now()
        self.admin = admin

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                os.environ.get('SECRET_KEY', "KEY"),
                algorithm='HS256'
            )
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            # Check Redis for auth token / user session data
            payload = jwt.decode(auth_token, os.environ.get('SECRET_KEY', "KEY"))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired.'
        except jwt.InvalidTokenError:
            return 'Invalid token.'

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}