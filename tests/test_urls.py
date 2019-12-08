import json
import responses

from base import BaseAPITest
from test_scan import INDEX_RESPONSE, VERSION_RESPONSE

from w3af_api_client import Connection, Scan


EXPECTED_URLS = ['http://target.example/1', 'http://target.example/2']
URL_LIST_RESPONSE = json.dumps({'items': EXPECTED_URLS})


class TestURLListClient(BaseAPITest):

    @responses.activate
    def test_url_list(self):
        responses.add(responses.GET,
                               self.get_url('/'),
                               body=INDEX_RESPONSE,
                               content_type='application/json')

        responses.add(responses.GET,
                               self.get_url('/version'),
                               body=VERSION_RESPONSE,
                               content_type='application/json')

        responses.add(responses.GET,
                               self.get_url('/scans/0/urls/'),
                               body=URL_LIST_RESPONSE,
                               content_type='application/json')

        conn = Connection(self.api_url)

        scan = Scan(conn, scan_id=0)
        urls = scan.get_urls()

        self.assertEqual(urls, EXPECTED_URLS)
