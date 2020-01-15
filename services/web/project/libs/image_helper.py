import os
import re
from werkzeug.datastructures import FileStorage
import uuid

from flask_uploads import UploadSet, IMAGES

IMAGE_SET = UploadSet("images", IMAGES)  # set name and allowed extensions


def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    """
    This method stores the image
    param: the file, the folder name, the name of the file
    return: the path to where the image was saved
    """
    name = str(uuid.uuid4()) + get_extension(image.filename)
    return IMAGE_SET.save(image, folder, name)


def get_extension(filename):
    """
    This method is to get the extension of a filename
    param id: string filename
    Return: file's extension
    get_extension('image.jpg') returns '.jpg'
    """
    return os.path.splitext(filename)[1]

def generate_guid(file):
    """
    This method is to generate the guid for storing images
    param id: the image file
    return: the guid for storing the file
    """
    return str(uuid.uuid4()) + get_extension(file.filename)
