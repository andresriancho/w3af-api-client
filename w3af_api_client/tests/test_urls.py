import json
import httpretty

from w3af_api_client import Connection, Scan
from w3af_api_client.tests.base import BaseAPITest
from w3af_api_client.tests.test_scan import INDEX_RESPONSE, VERSION_RESPONSE


EXPECTED_URLS = ['http://target.example/1', 'http://target.example/2']
URL_LIST_RESPONSE = json.dumps({'items': EXPECTED_URLS})


class TestURLListClient(BaseAPITest):

    @httpretty.activate
    def test_url_list(self):
        httpretty.register_uri(httpretty.GET,
                               self.get_url('/'),
                               body=INDEX_RESPONSE,
                               content_type='application/json')

        httpretty.register_uri(httpretty.GET,
                               self.get_url('/version'),
                               body=VERSION_RESPONSE,
                               content_type='application/json')

        httpretty.register_uri(httpretty.GET,
                               self.get_url('/scans/0/urls/'),
                               body=URL_LIST_RESPONSE,
                               content_type='application/json')

        conn = Connection(self.api_url)

        scan = Scan(conn, scan_id=0)
        urls = scan.get_urls()

        self.assertEqual(urls, EXPECTED_URLS)
