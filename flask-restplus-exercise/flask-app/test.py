import unittest
import json
from unittest.mock import patch

from app import flask_app


class BooksTests(unittest.TestCase):

    def setUp(self):
        self.app = flask_app.test_client()

    def test_astronauts_empty_params(self):
        response = self.app.get('/astronauts')
        assert response.status_code == 400

    def test_astronauts_invalid_params(self):
        response = self.app.get('/astronauts?country=1234')
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert not data

    def test_astronauts_valid_params(self):
        response = self.app.get('/astronauts?country=United-States-of-America')
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert "Not a name" not in data.get("San Diego")
        assert "William C. McCool" in data.get("San Diego")

    @patch('app.get_astronauts_by_country')
    def test_group_astronauts_by_city(self, mock_get_astronauts_by_country):
        with open('astronaut-USA.json') as f:
            mock_data = json.load(f)
        mock_get_astronauts_by_country.return_value = mock_data
        response = self.app.get('/astronauts?country=United-States-of-America')
        data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert "Not a name" not in data.get("San Diego")
        assert "William C. McCool" in data.get("San Diego")


if __name__ == "__main__":
    unittest.main()
