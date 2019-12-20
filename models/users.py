from app import db
import time
from exceptions import TokenNotFound
from helpers import _epoch_utc_to_datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import decode_token

class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(120), index=True, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    @classmethod
    def add_user_to_db(cls, data_username, data_email, data_password):
        user = User(
            username = data_username,
            email = data_email,
            password = data_password
        )
        db.session.add(user)
        db.session.commit()

    @classmethod
    def check_user_exist(cls, username):
        user = cls.query.filter_by(username = username).first()
        if user is None:
            return False
        else:
            return True

    @classmethod
    def verify_user_password(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return user
        else:
            return None

    def __repr__(self):
        return '<User {}>'.format(self.username)