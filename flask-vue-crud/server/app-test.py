import unittest
import os
from app import app


class BasicTestCase(unittest.TestCase):

    def test_ping(self):
        tester = app.test_client(self)
        response = tester.get('/ping', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'pong')

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 404)

    def test_database(self):
        tester = os.path.exists('flask-vue.db')
        self.assertTrue(tester)


if __name__ == '__main__':
    unittest.main()
