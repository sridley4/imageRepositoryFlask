from app import db
import time
from exceptions import TokenNotFound
from helpers import _epoch_utc_to_datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import decode_token

class BlacklistToken(db.Model):
    __tablename__ = 'blacklist_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    @classmethod
    def add_token_to_database(cls, encoded_token, identity_claim):
        """
        Adds a new token to the database. It is not revoked when it is added.
        :param identity_claim:
        """
        decoded_token = decode_token(encoded_token)
        jti = decoded_token['jti']
        token_type = decoded_token['type']
        user_identity = decoded_token[identity_claim]
        expires = _epoch_utc_to_datetime(decoded_token['exp'])
        revoked = False

        db_token = BlacklistToken(
            jti=jti,
            token_type=token_type,
            user_identity=user_identity,
            expires=expires,
            revoked=revoked,
        )
        db.session.add(db_token)
        db.session.commit()

    @classmethod
    def is_token_revoked(cls, decoded_token):
        """
        Checks if the given token is revoked or not. Because we are adding all the
        tokens that we create into this database, if the token is not present
        in the database we are going to consider it revoked, as we don't know where
        it was created.
        """
        jti = decoded_token['jti']
        try:
            token = cls.query.filter_by(jti=jti).one()
            return token.revoked
        except NoResultFound:
            return True

    @classmethod
    def get_user_tokens(cls, user_identity):
        """
        Returns all of the tokens, revoked and unrevoked, that are stored for the
        given user
        """
        return cls.query.filter_by(user_identity=user_identity).all()

    @classmethod
    def revoke_token(cls, token_id, user):
        """
        Revokes the given token. Raises a TokenNotFound error if the token does
        not exist in the database
        """
        try:
            token = cls.query.filter_by(id=token_id, user_identity=user).one()
            token.revoked = True
            db.session.commit()
        except NoResultFound:
            raise TokenNotFound("Could not find the token {}".format(token_id))

    @classmethod
    def prune_database(cls):
        """
        Delete tokens that have expired from the database.
        How (and if) you call this is entirely up you. You could expose it to an
        endpoint that only administrators could call, you could run it as a cron,
        set it up with flask cli, etc.
        """
        now = datetime.now()
        expired = cls.query.filter(cls.expires < now).all()
        for token in expired:
            db.session.delete(token)
        db.session.commit()