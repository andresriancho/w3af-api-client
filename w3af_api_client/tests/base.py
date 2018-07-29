import unittest
import urllib.parse
import json


class BaseAPITest(unittest.TestCase):

    def setUp(self):
        super(BaseAPITest, self).setUp()
        self.api_url = 'http://127.0.0.1:5001/'

    def get_url(self, path):
        return urllib.parse.urljoin(self.api_url, path)

    def assertJSONEquals(self, request, expected_json):
        self.assertEqual(json.loads(request.body),
                         expected_json)
