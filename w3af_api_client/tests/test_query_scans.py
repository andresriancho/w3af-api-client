import json
import unittest
import urlparse
import httpretty

from w3af_api_client import Connection
from w3af_api_client.tests.test_scan import INDEX_RESPONSE, VERSION_RESPONSE


SCAN_LIST_RESPONSE = json.dumps({'items': [{'id': 0,
                                            'href': '/scans/0',
                                            'target_urls': [''],
                                            'status': 'Running',
                                            'errors': True},

                                           {'id': 1,
                                            'href': '/scans/1',
                                            'target_urls': [''],
                                            'status': 'Stopped',
                                            'errors': False}
                                           ]})


class TestScanListClient(unittest.TestCase):

    def setUp(self):
        super(TestScanListClient, self).setUp()
        self.api_url = 'http://127.0.0.1:5001/'

    def get_url(self, path):
        return urlparse.urljoin(self.api_url, path)

    def assertJSONEquals(self, request, expected_json):
        self.assertEqual(json.loads(request.body),
                         expected_json)

    @httpretty.activate
    def test_scan_list(self):
        httpretty.register_uri(httpretty.GET,
                               self.get_url('/'),
                               body=INDEX_RESPONSE,
                               content_type='application/json')

        httpretty.register_uri(httpretty.GET,
                               self.get_url('/version'),
                               body=VERSION_RESPONSE,
                               content_type='application/json')

        httpretty.register_uri(httpretty.GET,
                               self.get_url('/scans/'),
                               body=SCAN_LIST_RESPONSE,
                               content_type='application/json')

        conn = Connection(self.api_url)

        scans = conn.get_scans()
        self.assertEqual([s.status for s in scans], ['Running', 'Stopped'])
        self.assertEqual([s.scan_id for s in scans], [0, 1])
