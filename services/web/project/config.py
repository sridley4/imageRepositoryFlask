import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = f"{os.getenv('APP_FOLDER')}/project/static"
    SECRET_KEY = "my_super_secret_key"
    JWT_SECRET_KEY = "my_super_secret_key"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    PROPAGATE_EXCEPTIONS = True