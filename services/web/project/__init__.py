from flask import Flask, make_response
import os
import json
from flask_restful import Api
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
#from flask_uploads import configure_uploads, patch_request_class
from project.resources.image import ImageUpload, AllImages, GetSpecificImage
from project.resources.album import CreateAlbum, GetAllAlbums, GetAlbum
#from project.libs.image_helper import IMAGE_SET

from project.resources.registration import UserRegistration
from project.resources.user_access import UserLogin, UserLogoutAccess

from project.models.black_list_token import BlacklistToken
from project.ma import ma
from project.db import db

app = Flask(__name__)

CORS(app)

api = Api(app)

jwt = JWTManager(app)

app.config.from_object("project.config.Config")
db.init_app(app)
ma.init_app(app)

api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogoutAccess, '/logout/access')
api.add_resource(ImageUpload, "/upload/image")
api.add_resource(AllImages, "/allimages")
api.add_resource(CreateAlbum, "/create_album")
api.add_resource(GetAllAlbums, "/get_albums")
api.add_resource(GetAlbum, "/get_album/<int:album_id>")
api.add_resource(GetSpecificImage, "/upload/<path:filename>")

@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return BlacklistToken.is_token_revoked(decoded_token)