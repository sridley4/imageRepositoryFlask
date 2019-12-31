from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)

class ImageId(ma.Schema):
    image_id = ma.Integer()

class AlbumCreateRequest(ma.Schema):
    title = ma.String()
    image_id = ma.Integer()
    image_id_list = ma.Pluck("self", "image_id", many=True)

class UserSchema(ma.Schema):
    name = ma.String()
    friends = ma.Pluck("self", "name", many=True)


db.create_all()
if __name__ == '__main__':
    schema = AlbumCreateRequest()
    data = {
     "title": "Steve",
     "image_id_list": [1, 2]
    }
    schema_data = schema.load(data)
    print(schema_data['image_id_list'])
    for image in schema_data['image_id_list']:
        print(image['image_id'])
    # <Parent (transient 4583120144)>