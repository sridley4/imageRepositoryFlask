from project.db import db
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound

albums_to_images = db.Table('albums_to_images',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id')),
    db.Column('image_id', db.Integer, db.ForeignKey('image.id'))
)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    username = db.Column(db.String(140), db.ForeignKey('users.username'))
    first_image_location = db.Column(db.String(140))
    images = db.relationship('Image', secondary=albums_to_images, backref=db.backref('album_images', lazy='dynamic'))
    
    @classmethod
    def get_all_albums_for_user(cls, user):
        return cls.query.filter_by(username=user).all()
    
    @classmethod
    def get_album_by_id(cls, album_id):
        return cls.query.filter_by(id=album_id).first()
    
    @classmethod
    def get_all_images(cls, album_id):
        return cls.query.filter_by(id=album_id).first().images
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()