import unittest
from project import app
from project.db import db

class TestAlbumService(unittest.TestCase):
    
    def test_get_albums(self):
        tester = app.test_client(self)
        response = tester.post('/login',json={
            'username': 'test_user', 'password': 'password'
        })
        json_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['login'], True)

        access_headers = {'Authorization': "Bearer " + json_data['access_token']}
        response = tester.get("/get_albums", headers=access_headers)
        json_data = response.get_json()
        album_list = json_data['albums']

        self.assertEqual(len(album_list),2)
        self.assertTrue(album_list[0]['id'])
        self.assertTrue(album_list[1]['id'])
        self.assertEqual(album_list[0]['title'], "album_title")
        self.assertEqual(album_list[1]['title'], "album_title2")
        self.assertEqual(album_list[0]['first_image_location'], "/image_path/test1")
        self.assertEqual(album_list[1]['first_image_location'], "/image_path/test2")
    
    def test_get_specific_album(self):
        tester = app.test_client(self)
        response = tester.post('/login',json={
            'username': 'test_user', 'password': 'password'
        })
        json_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['login'], True)

        access_headers = {'Authorization': "Bearer " + json_data['access_token']}
        response = tester.get("/get_albums", headers=access_headers)
        json_data = response.get_json()
        album_list = json_data['albums']

        response = tester.get("/get_album/" + str(album_list[0]['id']), headers=access_headers)
        json_data = response.get_json()
        album = json_data['album']
        images_list = json_data['images']

        self.assertEqual(album['title'], "album_title")
        self.assertEqual(album['id'], album_list[0]['id'])

        self.assertEqual(len(images_list),2)
        self.assertTrue(images_list[0]['id'])
        self.assertTrue(images_list[1]['id'])
        self.assertEqual(images_list[0]['title'], "title_test")
        self.assertEqual(images_list[1]['title'], "title_test2")
        self.assertEqual(images_list[0]['url_location'], "/image_path/test1")
        self.assertEqual(images_list[1]['url_location'], "/image_path/test2")
    
    def test_get_specific_album_unauthorized(self):
        tester = app.test_client(self)
        response = tester.post('/login',json={
            'username': 'test_user2', 'password': 'password2'
        })
        json_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['login'], True)

        access_headers = {'Authorization': "Bearer " + json_data['access_token']}
        response = tester.get("/get_album/1", headers=access_headers)
        json_data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json_data['message'], "This is not your album.")
        



