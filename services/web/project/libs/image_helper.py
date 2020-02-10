import os
import re
from werkzeug.datastructures import FileStorage
import uuid
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif'}

UPLOAD_FOLDER = f"{os.getenv('APP_FOLDER')}/project/static/"


def save_image(file: FileStorage) -> str:
    """
    This method stores the image
    param: the file, the folder name, the name of the file
    return: the path to where the image was saved
    """
    name = str(uuid.uuid4()) + get_extension(file.filename)

    filename = secure_filename(name)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return str(UPLOAD_FOLDER + name)

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
