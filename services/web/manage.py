from flask.cli import FlaskGroup
import unittest

from project import app
from project.db import db

from project.models.albums import Album
from project.models.images import Image
from project.models.users import UserModel

from project.libs.user_helpers import _generate_password

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    """Seed the database with mock data"""
    usermock = UserModel(username="test_user", email="test@email.com", password=_generate_password("password"))
    usermock.save_to_db()
    
    usermock2 = UserModel(username="test_user2", email="test2@email.com", password=_generate_password("password2"))
    usermock2.save_to_db()

    image1 = Image(title="title_test", url_location="/image_path/test1", username=usermock.username)
    image2 = Image(title="title_test2", url_location="/image_path/test2", username=usermock.username)
    image3 = Image(title="title_test3", url_location="/image_path/test3", username=usermock.username)
    image4 = Image(title="title_test4", url_location="/image_path/test4", username=usermock2.username)

    image1.save_to_db()
    image2.save_to_db()
    image3.save_to_db()
    image4.save_to_db()

    album1 = Album(title="album_title", username=usermock.username, first_image_location=image1.url_location)
    album1.images.append(image1)
    album1.images.append(image2)

    album1.save_to_db()

    album2 = Album(title="album_title2", username=usermock.username, first_image_location=image2.url_location)
    album2.images.append(image2)
    album2.images.append(image3)

    album2.save_to_db()

@cli.command("run_tests")
def test():

    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover('project/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    cli()