import unittest
from project import app
from project.db import db


class TestRegistrationService(unittest.TestCase):
    
    def test_register(self):
        tester = app.test_client(self)
        response = tester.post('/registration',json={
        'username': 'hello', 'email':'example@example.com', 'password': 'secret'
        })
        json_data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_data['message'], "Account created successfully.")

    def test_register_username_taken(self):
        tester = app.test_client(self)
        #test to make sure we can't create a user with a username already registered
        response = tester.post('/registration',json={
        'username': 'test_user', 'email':'someone@example.com', 'password': 'secret'
        })
        json_data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_data['message'], "A user with that username already exists.")

    def test_register_email_taken(self):
        tester = app.test_client(self)
        #test to make sure we can't create a user with an email already registered
        response = tester.post('/registration',json={
        'username': 'newuser', 'email':'test@email.com', 'password': 'secret'
        })
        json_data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_data['message'], "A user with that email already exists.")

