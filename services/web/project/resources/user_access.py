from flask import Flask, request
from flask_restful import Resource
from project.models.users import UserModel
from project.schema.user import UserSchema
from project.models.black_list_token import BlacklistToken
import traceback
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from project.libs.strings import gettext

user_schema = UserSchema()

class UserLogin(Resource):

    def post(self):
        """
        Allows the user to login provided they have correct credentials
        Example of json is:
        {
	        "username":"test_user",
	        "password":"password"
        }
        """
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=("email",))

        current_user = UserModel.authenticate_user(user_data.username, user_data.password)

        if not current_user:
            return {
                'login': False,
                'message': gettext("user_invalid_credentials")
            }, 400
        else:
            access_token = create_access_token(identity = user_data.username)
            refresh_token = create_refresh_token(identity = user_data.username)

            BlacklistToken.add_token_to_database(access_token, user_data.username)
            BlacklistToken.add_token_to_database(refresh_token, user_data.username)
            return {
                'login': True,
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

class UserLogoutAccess(Resource):
    @jwt_required
    def get(self):
        """
        Allows the user to logout, it revokes the associated token
        """
        token_id = get_raw_jwt()['jti']
        user_identity = get_jwt_identity()
        try:
            BlacklistToken.revoke_token(token_id, user_identity)
            return {
                'login': False,
                'message': gettext("user_logged_out").format(user_identity)
            }, 200
        except:
            traceback.print_exc()
            return {"message": gettext("server_error")}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def get(self):
        """
        Allows the user to get a new access token provided they have non expired refresh token
        """
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = BlacklistToken(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {"message": gettext("server_error")}, 500