import unittest
from project import app
from project.db import db

class TestUserService(unittest.TestCase):
    
    def test_login(self):
        tester = app.test_client(self)
        response = tester.post('/login',json={
            'username': 'test_user', 'password': 'password'
        })
        json_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['login'], True)
        self.assertTrue(json_data['access_token'])
        self.assertTrue(json_data['refresh_token'])
    
    def test_false_login(self):
        tester = app.test_client(self)
        response = tester.post('/login',json={
            'username': 'test_user', 'password': 'not_the_password'
        })
        json_data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_data['login'], False)
        self.assertTrue(json_data['message'], "Invalid username or password")
    
    def test_logout(self):
        tester = app.test_client(self)
        response = tester.post('/login',json={
            'username': 'test_user', 'password': 'password'
        })
        json_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['login'], True)

        access_headers = {'Authorization': "Bearer " + json_data['access_token']}
        response = tester.get("/logout/access", headers=access_headers)
        json_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['login'], False)
        self.assertEqual(json_data['message'], "User test_user successfully logged out and tokens revoked.")

        response = tester.get("/get_albums", headers=access_headers)
        self.assertEqual(response.status_code, 401)
        json_data = response.get_json()
        self.assertEqual(json_data['msg'], "Token has been revoked")

    def test_false_logout(self):
        tester = app.test_client(self)
        response = tester.post('/login',json={
            'username': 'test_user', 'password': 'password'
        })
        json_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['login'], True)

        access_headers = {'Authorization': "Bearer " + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzgwOTMzNDcsIm5iZiI6MTU3ODA5MzM0NywianRpIjoiMTM2MGJhMDItOTIzZS00N2RjLWI3NjMtZmE1ODAxNjc0MzExIiwiZXhwIjoxNTc4MDk0MjQ3LCJpZGVudGl0eSI6ImhlbGxvIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.KfSz6JhknPK0d2RQ3jDoMNrtvEXzWr3QzhWJ_RXt0_c"}
        response = tester.get("/logout/access", headers=access_headers)
        json_data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json_data['msg'], "Token has expired")

        access_headers = {'Authorization': "Bearer " + "somethingrandom"}
        response = tester.get("/logout/access", headers=access_headers)
        json_data = response.get_json()
        self.assertEqual(response.status_code, 422)
        self.assertEqual(json_data['msg'], "Not enough segments")
