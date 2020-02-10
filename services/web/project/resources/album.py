from flask_restful import Resource, reqparse
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback



from project.schema.album_create import AlbumCreateRequest
from project.schema.image import ImageSchema
from project.schema.album import AlbumSchema
from project.models.albums import Album
from project.models.images import Image
from project.libs.strings import gettext

album_request_schema = AlbumCreateRequest()

class CreateAlbum(Resource):
    @jwt_required
    def post(self):
        """
        Creates the album with the information provided by the client
        required are title, and image_id_list: list of image ids
        Example of post json is
        {
	        "title":"secondalbum",
	        "image_id_list":[2,3]
        }
        """
        user_id = get_jwt_identity()
        
        try:
            data = album_request_schema.load(request.get_json())
            album_image_id = data['image_id_list'][0]['image_id']
            album_image = Image.get_image_by_id(album_image_id)

            album = Album(title=data['title'], username=user_id, first_image_location=album_image.url_location)

            for image in data['image_id_list']:
                retrieved_image = Image.get_image_by_id(image['image_id'])
                album.images.append(retrieved_image)
            album.save_to_db()
        
            return {"message": gettext("album_created").format(data['title'])}, 201
        except:
            traceback.print_exc()
            return {"message": gettext("album_error_creation")}, 500

albums_schema = AlbumSchema(many=True, only=("id", "title", "first_image_location"))

class GetAllAlbums(Resource):
    @jwt_required
    def get(self):
        """
        Gets all associated albums connected to user
        """
        user_id = get_jwt_identity()
        

        try:
            user_albums = Album.get_all_albums_for_user(user_id)
        
            albums = albums_schema.dump(user_albums)
            return {"albums": albums},201
        except:
            traceback.print_exc()
            return {"message": gettext("album_error_retrieval")}, 500


album_schema = AlbumSchema(only=("title", "id"))
image_schema = ImageSchema(many=True, only=("id", "title", "url_location"))

class GetAlbum(Resource):
    @classmethod
    @jwt_required
    def get(cls, album_id: int):
        """
        Gets specific album passed by album id
        """
        album = Album.get_album_by_id(album_id)

        user_id = get_jwt_identity()

        album_images=Album.get_all_images(album_id)

        if(album.username!=user_id):
            return {'message': gettext("album_unauthorized_access")}, 401

        album_result = album_schema.dump(album)
        images_result = image_schema.dump(album_images)
        try: 
            return{'album': album_result, 'images': images_result}, 201
        except:
            return {"message": gettext("album_error_retrieval")}, 500
        
