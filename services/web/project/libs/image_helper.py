import os
import re
from werkzeug.datastructures import FileStorage
import uuid

from flask_uploads import UploadSet, IMAGES

IMAGE_SET = UploadSet("images", IMAGES)  # set name and allowed extensions


def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    name = str(uuid.uuid4()) + get_extension(image.filename)
    return IMAGE_SET.save(image, folder, name)


def get_extension(filename):
    """
    Return file's extension, for example
    get_extension('image.jpg') returns '.jpg'
    """
    return os.path.splitext(filename)[1]

def generate_guid(file):
    return str(uuid.uuid4()) + get_extension(file.filename)
