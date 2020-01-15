from flask_restful import Resource, reqparse
from flask_uploads import UploadNotAllowed
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.datastructures import FileStorage
import traceback

from project.schema.image_request import ImageRequestSchema
from project.schema.image import ImageSchema
from project.libs import image_helper
from project.models.images import Image
from project.libs.strings import gettext

image_request_schema = ImageRequestSchema()

class ImageUpload(Resource):
    @jwt_required
    def post(self):
        """
        This endpoint is used to upload an image file. It uses the
        JWT to retrieve user information and save the image in the user's folder.
        If a file with the same name exists in the user's folder, name conflicts
        will be automatically resolved by appending a underscore and a smallest
        unused integer. (eg. filename.png to filename_1.png).
        """
        data = image_request_schema.load(request.files)
        user_id = get_jwt_identity()
        title = request.form['title']
        try:
            # save(self, storage, folder=None, name=None)
            image_path = image_helper.save_image(data["image"], name=image_helper.generate_guid(data["image"]))
            image = Image(title=title, url_location=image_path, username=user_id)
            image.save_to_db()
            return {"message": gettext("image_uploaded").format(image.title)}, 201
        except UploadNotAllowed:  # forbidden file type
            extension = image_helper.get_extension(data["image"])
            return {"message": gettext("image_illegal_extension").format(extension)}, 400
        except:
            traceback.print_exc()
            return {"message": gettext("server_error")}, 500

image_schema = ImageSchema(many=True, only=("id", "title", "url_location"))

class AllImages(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user_images = Image.get_all_images_for_user(user_id)
        
        result = image_schema.dump(user_images, many=True)

        try:
            return {"images": result},201
        except:
            traceback.print_exc()
            return {"message": gettext("server_error")}, 500