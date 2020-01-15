import unittest
from project import app
from project.db import db

class TestImageService(unittest.TestCase):
    def test_get_images(self):
        tester = app.test_client(self)
        response = tester.post('/login',json={
            'username': 'test_user', 'password': 'password'
        })
        json_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['login'], True)

        access_headers = {'Authorization': "Bearer " + json_data['access_token']}
        response = tester.get("/allimages", headers=access_headers)
        json_data = response.get_json()

        image_list = json_data['images']

        self.assertEqual(len(image_list),3)
        self.assertTrue(image_list[0]['id'])
        self.assertTrue(image_list[1]['id'])
        self.assertTrue(image_list[2]['id'])
        self.assertEqual(image_list[0]['title'], "title_test")
        self.assertEqual(image_list[1]['title'], "title_test2")
        self.assertEqual(image_list[2]['title'], "title_test3")
        self.assertEqual(image_list[0]['url_location'], "/image_path/test1")
        self.assertEqual(image_list[1]['url_location'], "/image_path/test2")
        self.assertEqual(image_list[2]['url_location'], "/image_path/test3")