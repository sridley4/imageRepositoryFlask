from app import db
import time
from exceptions import TokenNotFound
from helpers import _epoch_utc_to_datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import decode_token


# album_to_image = db.Table('albums_to_image_table',
#                           db.Column('image_id', db.Integer, db.ForeignKey('image.id')),
#                           db.Column('album_id', db.Integer, db.ForeignKey('album.id')))


# class Album(db.Model):
#     __tablename__ = 'albums'
#     id = db.Column(db.Integer, primary_key=True)
#     location = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=db.datetime.utcnow)
#     user_id = db.Column(db.String(140), db.ForeignKey('users.username'))
#     images = db.relationship('Image',secondary=album_to_image, lazy='dynamic')

#     @classmethod
#     def get_all_images_for_album(cls, album):
#         return cls.query.filber_by(id=)



class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    location = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=db.datetime.utcnow)
    user_id = db.Column(db.String(140), db.ForeignKey('users.username'))
    # albums = db.relationship('Album',secondary=album_to_image, lazy='dynamic')
    
    @classmethod
    def get_all_images_for_user(cls, user):
        return cls.query.filter_by(user=user.username).all()
    
    @classmethod
    def add_image_to_db(cls, image_name, username):
        image = Image(
            location = image_name,
            user_id = username
        )
        db.session.add(image)
        db.session.commit()

    def __repr__(self):
        return '<Image {}>'.format(self.location, self.user_id)