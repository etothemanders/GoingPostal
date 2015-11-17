import os
import tempfile
import unittest

from app import app
from app.model import create_db


class TestViews(unittest.TestCase):

    def setUp(self):
        self.db_test, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        create_db()

    def tearDown(self):
        os.close(self.db_test)
        os.unlink(app.config['DATABASE'])

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_index(self):
        response = self.app.get('/')
        assert response.status_code == 200
        assert 'Package tracking for online shoppers' in response.data

    def test_login(self):
        response = self.app.get('/login')
        assert response.status_code == 302
        assert 'You should be redirected automatically to target URL: <a href="https://accounts.google.com/o/oauth2/auth' in response.data

    def test_logout(self):
        response = self.logout()
        assert response.status_code == 200
        assert 'Package tracking for online shoppers' in response.data

if __name__ == '__main__':
    unittest.main()
