from db import db
import time
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import decode_token



class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    url_location = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    username = db.Column(db.String(140), db.ForeignKey('users.username'))
    
    @classmethod
    def get_all_images_for_user(cls, user):
        return cls.query.filter_by(username=user).all()
    
    @classmethod
    def get_image_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return '<Image {}>'.format(self.location, self.user_id)