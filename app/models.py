from app import db
import time
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(120), index=True, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

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


class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=db.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    @classmethod
    def get_all_images_for_user(cls, user):
        return cls.query.filter_by(user_id=user.id).all()

    def __repr__(self):
        return '<Image {}>'.format(self.location, self.user_id)

class BlacklistToken(db.Model):
    __tablename__ = 'blacklist_tokens'
    id = db.Column(db.Integer, primary_key = True)
    token = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, token):
        query = cls.query.filter_by(token = token).first()
        return bool(query)