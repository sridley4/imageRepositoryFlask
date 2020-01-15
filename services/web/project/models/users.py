from project.db import db
from werkzeug.security import check_password_hash

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        """
        Finds the user by username
        """
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_email(cls, email):
        """
        Finds the user by email
        """
        return cls.query.filter_by(email=email).first()

    @classmethod
    def authenticate_user(cls, username, password):
        """
        Checks if the corrects username and password were entered
        """
        user = cls.find_by_username(username)
        if user is not None and check_password_hash(user.password, password):
            return user
        else:
            return None


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()