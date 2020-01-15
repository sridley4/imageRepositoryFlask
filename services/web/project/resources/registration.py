from flask import Flask, request
from flask_restful import Resource
import traceback
from project.models.users import UserModel
from project.schema.user import UserSchema
from project.libs.user_helpers import _generate_password
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from project.libs.strings import gettext

user_schema = UserSchema()

class UserRegistration(Resource):
    
    @classmethod
    def post(cls):
        """
        Allows the cleint to create a user account
        Example json attached to post:
        {
	        "username":"hello",
	        "email":"email@exmaple",
	        "password":"password"
        }
        """
        user_json = request.get_json()
        try:
            user = user_schema.load(user_json)

            if UserModel.find_by_username(user.username):
                return {"message": gettext("user_username_exists")}, 400
            if UserModel.find_by_email(user.email):
                return {"message": gettext("user_email_exists")}, 400
        
            user.password = _generate_password(user.password)
            user.save_to_db()

            return {"message": gettext("user_registered")}, 201
        except:
            traceback.print_exc()
            return {"message": gettext("user_error_creating")}, 500