import json
import base64
import httpretty

from w3af_api_client import Connection, Scan
from w3af_api_client.tests.base import BaseAPITest
from w3af_api_client.tests.test_scan import INDEX_RESPONSE, VERSION_RESPONSE


EXPECTED_FRS = ['GET http://target.example/1 HTTP/1.1\r\nHost:target.example',
                'GET http://target.example/2 HTTP/1.1\r\nHost:target.example']
ENCODED_EXPECTED_FRS = [base64.b64encode(fr) for fr in EXPECTED_FRS]
FR_LIST_RESPONSE = json.dumps({'items': ENCODED_EXPECTED_FRS})


class TestFuzzableRequestListClient(BaseAPITest):

    @httpretty.activate
    def test_fuzzable_request_list(self):
        httpretty.register_uri(httpretty.GET,
                               self.get_url('/'),
                               body=INDEX_RESPONSE,
                               content_type='application/json')

        httpretty.register_uri(httpretty.GET,
                               self.get_url('/version'),
                               body=VERSION_RESPONSE,
                               content_type='application/json')

        httpretty.register_uri(httpretty.GET,
                               self.get_url('/scans/0/fuzzable-requests/'),
                               body=FR_LIST_RESPONSE,
                               content_type='application/json')

        conn = Connection(self.api_url)

        scan = Scan(conn, scan_id=0)
        frs = scan.get_fuzzable_requests()

        self.assertEqual(frs, EXPECTED_FRS)

