from flask import Flask
import os
from db import db
from ma import ma
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_uploads import configure_uploads, patch_request_class
from resources.image import ImageUpload, AllImages
from libs.image_helper import IMAGE_SET

from resources.registration import UserRegistration
from resources.user_access import UserLogin, UserLogoutAccess

from models.black_list_token import BlacklistToken



app = Flask(__name__)
api = Api(app)

app.config['UPLOADED_IMAGES_DEST'] = os.path.join("static", "images")

patch_request_class(app, 10 * 1024 * 1024)  # restrict max upload image size to 10MB
configure_uploads(app, IMAGE_SET)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

@app.before_first_request
def create_tables():
    db.create_all()

@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return BlacklistToken.is_token_revoked(decoded_token)

api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogoutAccess, '/logout/access')
api.add_resource(ImageUpload, "/upload/image")
api.add_resource(AllImages, "/allimages")
#api.add_resource(UserLogoutRefresh, '/logout/refresh')
#api.add_resource(TokenRefresh, '/token/refresh')

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)