from flask import Flask, request
from flask_restful import Resource
from models.users import UserModel
from schema.user import UserSchema
from models.black_list_token import BlacklistToken
import traceback
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

user_schema = UserSchema()

class UserLogin(Resource):

    def post(self):
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=("email",))

        current_user = UserModel.authenticate_user(user_data.username, user_data.password)

        if not current_user:
            return {'message': 'Invalid username or password'}
        else:
            access_token = create_access_token(identity = user_data.username)
            refresh_token = create_refresh_token(identity = user_data.username)

            BlacklistToken.add_token_to_database(access_token, user_data.username)
            BlacklistToken.add_token_to_database(refresh_token, user_data.username)
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        token_id = get_raw_jwt()['jti']
        user_identity = get_jwt_identity()
        try:
            BlacklistToken.revoke_token(token_id, user_identity)
            return {'msg': 'Token revoked'}, 200
        except:
            traceback.print_exc()
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