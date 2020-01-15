import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_IMAGES_DEST = f"{os.getenv('APP_FOLDER')}/project/static"
    SECRET_KEY = "my_super_secret_key"
    JWT_SECRET_KEY = "my_super_secret_key"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

# class TestingConfig(Object):
#     """Testing configuration"""
#     DEBUG = True
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
#     UPLOADED_IMAGES_DEST = f"{os.getenv('APP_FOLDER')}/project/static"
#     SECRET_KEY = "my_super_secret_key"
#     JWT_SECRET_KEY = "my_super_secret_key"
#     JWT_BLACKLIST_ENABLED = True
#     JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']