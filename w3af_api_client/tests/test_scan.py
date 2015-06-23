import json
import unittest
import urlparse
import httpretty


from w3af_api_client import Connection
from w3af_api_client import LogEntry, Log
from w3af_api_client import Scan
from w3af_api_client import Finding


SCAN_START_SUCCESS = json.dumps({u'message': u'Success',
                                 u'href': u'/scans/0',
                                 u'id': 0})

INDEX = json.dumps({'docs': 'http://docs.w3af.org/en/latest/api/index.html'})


class TestScanUsingClient(unittest.TestCase):

    def setUp(self):
        super(TestScanUsingClient, self).setUp()
        self.api_url = 'http://127.0.0.1:5001/'
        self.target_url = 'http://target.example/'

    def get_url(self, path):
        return urlparse.urljoin(self.api_url, path)

    @httpretty.activate
    def test_simple_scan(self):
        #
        # Mock all HTTP responses
        #
        httpretty.register_uri(httpretty.GET,
                               self.get_url('/'),
                               body=INDEX,
                               content_type='application/json')

        httpretty.register_uri(httpretty.POST,
                               self.get_url('/scans/'),
                               body=SCAN_START_SUCCESS,
                               content_type='application/json',
                               status=201)

        conn = Connection(self.api_url)
        #conn.set_verbose(True)

        self.assertTrue(conn.can_access_api())

        #
        #   Start a scan and assert
        #
        scan = Scan(conn)
        scan.start('mock_profile', [self.target_url])