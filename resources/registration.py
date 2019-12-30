from flask import Flask, request
from flask_restful import Resource, reqparse
from models.users import UserModel
from schema.user import UserSchema
from libs.user_helpers import _generate_password
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

user_schema = UserSchema()

class UserRegistration(Resource):
    
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)

        if UserModel.find_by_username(user.username):
            return {"message": "A user with that username already exists"}, 400
        if UserModel.find_by_email(user.email):
            return {"message": "A user with that email already exists"}, 400
        
        user.password = _generate_password(user.password)
        user.save_to_db()

        return {"message": "User created successfully."}, 201