from flask import Flask
from flask_restful import Resource, reqparse
from app.models import User, Image, BlacklistToken
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from helpers import allowed_file, get_extension
import os, hashlib
from app import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
import werkzeug

class UserRegistration(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("username")
        self.parser.add_argument("email")
        self.parser.add_argument("password")

    def post(self):
        data = self.parser.parse_args()
        
        if User.check_user_exist(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}
        
        try:
            User.add_user_to_db(data['username'], data['email'], data['password'])
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("username")
        self.parser.add_argument("password")

    def post(self):
        data = self.parser.parse_args()

        current_user = User.verify_user_password(data['username'], data['password'])

        if not current_user:
            return {'message': 'Invalid username or password'}
        else:
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = BlacklistToken(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = BlacklistToken(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

class UploadPicture(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("username")
        self.parser.add_argument("file", type=werkzeug.datastructures.FileStorage, location='files')

    @jwt_required
    def post(self):
        data = parser.parse_args()
        if data['file'] == "":
            return {
                    'data':'',
                    'message':'No file found',
                    'status':'error'
            }
        photo = data['file']
        

        if photo and allowed_file(photo.filename):
            filename = str(int(hashlib.sha256(photo.filename.encode('utf-8')).hexdigest(), 16) % (10 ** 8)) + get_extension(photo.filename)
            Image.add_image_to_db(filename, data['username'])
            photo.save(os.path.join(UPLOAD_FOLDER,filename))
            return {
                    'data':'',
                    'message':'photo uploaded',
                    'status':'success'
                    }
        return {
                'data':'',
                'message':'Something when wrong',
                'status':'error'
                }
        
        
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}