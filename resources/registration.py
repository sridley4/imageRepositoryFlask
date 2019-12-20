from flask import Flask
from flask_restful import Resource, reqparse
from models.users import User
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


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