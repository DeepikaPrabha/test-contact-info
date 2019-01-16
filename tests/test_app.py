
import unittest
import mock
import os
import app
import requests
from app import db as test_db
from app import app as test_app
from base64 import b64encode
from mock import patch
import auth
import json


TEST_DB = 'sqlite:///' + 'test.db'
env = {}
env['username'] = 'dummy'
env['password'] = '275876e34cf609db118f3d84b799a790'

hdr =  b64encode(b'dummy:dummy').decode('utf-8')
HEADER = {'Authorization': 'Basic {0}'.format(hdr)}

class AppTest(unittest.TestCase):

    def setUp(self):
        test_app.config['WTF_CSRF_ENABLED'] = False
        test_app.config['TESTING'] = True
        test_app.config['LOGIN_DISABLED'] = True
        test_app.config['DEBUG'] = True

        test_app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB

        self.client = test_app.test_client()
        self.test_app = test_app
        with self.test_app.app_context():
            test_db.create_all()
        self.assertEqual(test_app.debug, True)

    def tearDown(self):
        with self.test_app.app_context():
            test_db.drop_all()

    @patch('app.os')
    @patch('auth.os')
    def test_index(self, mock_os, mock_auth_us):
        mock_os.environ = env
        mock_auth_us = env
        res = self.client.get('/', headers=HEADER)

    @patch('app.os')
    @patch('auth.os')
    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_search_by_email(self, mock_get, mock_os, mock_auth_us):
        mock_os.environ = env
        mock_auth_us = env
        with self.test_app.test_client() as c:
            res = c.get('/search_by_email',  query_string=dict(email='dummy'))
        self.assertEqual(res.status_code, 200)
        res = self.client.get('/search_by_email')
        self.assertEqual(res.status_code, 200)
        with self.test_app.test_client() as c:
            res = c.get('/search_by_email',  query_string=dict(email=''))
        self.assertEqual(res.status_code, 200)

    @patch('app.os')
    @patch('auth.os')
    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_search_by_name(self, mock_get, mock_os, mock_auth_us):
        mock_os.environ = env
        mock_auth_us = env
        msg = dict(name='dummy', email='dummy@gmail.com', city='dummy')
        with self.test_app.test_client() as c:
            res = c.post('/add_user',  headers=HEADER,
                         query_string=msg, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        with self.test_app.test_client() as c:
            res = c.get('/search_by_name',  query_string=dict(name='dummy'))
        self.assertEqual(res.status_code, 200)

        with self.test_app.test_client() as c:
            res = c.get('/search_by_name',  query_string=dict(name=''))

        with self.test_app.test_client() as c:
            res = c.get('/search_by_name',  query_string={})
        self.assertEqual(res.status_code, 200)

    @patch('app.os')
    @patch('auth.os')
    def test_add_user(self, mock_os, mock_auth_us):
        mock_os.environ = env
        mock_auth_us = env
        msg = dict(name='dummy', email='dummy@gmail.com', city='dummy')
        with self.test_app.test_client() as c:
            res = c.post('/add_user',  headers=HEADER,
                         query_string=msg, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        with self.test_app.test_client() as c:
            res = c.post('/add_user',  headers=HEADER,
                         query_string={}, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        with self.test_app.test_client() as c:
            res = c.post('/add_user',  headers=HEADER)
        self.assertEqual(res.status_code, 200)

    @patch('flask_sqlalchemy._QueryProperty.__get__')
    @patch('app.os')
    @patch('auth.os')
    def test_add_user_with_model(self, mock_os, mock_auth_us, mock_query):
        mock_os.environ = env
        mock_auth_us = env
        user_info = dict(
            name='dummy1', email='dummy1@gmail.com', city='dummy1')

        mock_query.return_value.filter_by.return_value.first.return_value = "some"
        with self.test_app.test_client() as c:
            res = c.post('/add_user', headers=HEADER,
                         query_string=user_info, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            res.data, b"email id already exist, please use something else")

        with self.test_app.test_client() as c:
            res = c.post('/add_user', headers=HEADER,
                         query_string={}, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            res.data, b"Missing one of these arguments, name = [None], email = [None], city = [None]")

    @patch('app.os')
    @patch('auth.os')
    def test_add_user_with_model_data(self, mock_os, mock_auth_us):
        mock_os.environ = env
        mock_auth_us = env
        user_info = dict(
            name='dummy123', email='dummy@gmail.com', city='dummy')
        msg = dict(email='dummy123@gmail.com')

        with self.test_app.test_client() as c:
            res = c.post('/add_user',  headers=HEADER,
                         query_string=user_info, content_type='application/json')
        self.assertEqual(res.status_code, 200)

    @patch('app.os')
    @patch('auth.os')
    def test_update_user(self, mock_os, mock_auth_us):
        mock_os.environ = env
        mock_auth_us = env
        msg = dict(name='dummy123', email='dummy@gmail.com')
        with self.test_app.test_client() as c:
            res = c.put('/update_user',  headers=HEADER,
                        query_string=msg, content_type='application/json')
        self.assertEqual(res.status_code, 200)

        with self.test_app.test_client() as c:
            res = c.put('/update_user', headers=HEADER,
                        query_string={}, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        with self.test_app.test_client() as c:
            res = c.put('/update_user',  headers=HEADER)
        self.assertEqual(res.status_code, 200)

    @patch('app.os')
    @patch('auth.os')
    def test_update_user_with_model_data(self, mock_os, mock_auth_us):
        mock_os.environ = env
        mock_auth_us = env
        user_info = dict(
            name='dummy123', email='dummy123@gmail.com', city='dummy')
        msg = dict(email='dummy123@gmail.com', name='new dummy')

        with self.test_app.test_client() as c:
            res = c.post('/add_user',  headers=HEADER,
                         query_string=user_info, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        with self.test_app.test_client() as c:
            res = c.put('/update_user', headers=HEADER,
                        query_string=msg, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b"Updated User new dummy successfully")

        msg = dict(city='dummy123', email='dummy123@gmail.com')
        with self.test_app.test_client() as c:
            res = c.put('/update_user',  headers=HEADER,
                        query_string=msg, content_type='application/json')
        self.assertEqual(res.status_code, 200)

    @patch('app.os')
    @patch('auth.os')
    def test_delete_user(self, mock_os, mock_auth_us):
        mock_os.environ = env
        mock_auth_us = env
        msg = dict(email='dummy@gmail.com')
        with self.test_app.test_client() as c:
            res = c.delete('/delete_user',  headers=HEADER,
                           query_string=msg, content_type='application/json')
        self.assertEqual(res.status_code, 200)

        with self.test_app.test_client() as c:
            res = c.delete('/delete_user',  headers=HEADER)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b"Missing email in request, discarding")

    @patch('flask_sqlalchemy._QueryProperty.__get__')
    @patch('app.os')
    @patch('auth.os')
    def test_delete_user_with_model(self, mock_os, mock_auth_us, mock_query):
        mock_os.environ = env
        mock_auth_us = env
        user_info = dict(name='dummy', email='dummy@gmail.com', city='dummy')
        msg = dict(email='dummy@gmail.com')
        mock_query.return_value.filter_by.return_value.first.return_value = []
        with self.test_app.test_client() as c:
            res = c.delete('/delete_user', headers=HEADER,
                           query_string=msg, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b"No such user exist")

    @patch('app.os')
    @patch('auth.os')
    def test_delete_user_with_model_data(self, mock_os, mock_auth_us):
        mock_os.environ = env
        mock_auth_us = env
        user_info = dict(
            name='dummy123', email='dummy123@gmail.com', city='dummy')
        msg = dict(email='dummy123@gmail.com')

        with self.test_app.test_client() as c:
            res = c.post('/add_user',  headers=HEADER,
                         query_string=user_info, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        with self.test_app.test_client() as c:
            res = c.delete('/delete_user', headers=HEADER,
                           query_string=msg, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b"Deleted user successfully")


if __name__ == '__main__':
    unittest.main()
