import json
import base64
import responses
from base import BaseAPITest
from test_scan import INDEX_RESPONSE, VERSION_RESPONSE

from w3af_api_client import Connection, Scan


EXPECTED_FRS = ['GET http://target.example/1 HTTP/1.1\r\nHost:target.example',
                'GET http://target.example/2 HTTP/1.1\r\nHost:target.example']
ENCODED_EXPECTED_FRS = [base64.b64encode(fr.encode('utf-8')).decode('utf-8') for fr in EXPECTED_FRS]
FR_LIST_RESPONSE = json.dumps({'items': ENCODED_EXPECTED_FRS})


class TestFuzzableRequestListClient(BaseAPITest):

    @responses.activate
    def test_fuzzable_request_list(self):
        responses.add(responses.GET,
                               self.get_url('/'),
                               body=INDEX_RESPONSE,
                               content_type='application/json')

        responses.add(responses.GET,
                               self.get_url('/version'),
                               body=VERSION_RESPONSE,
                               content_type='application/json')

        responses.add(responses.GET,
                               self.get_url('/scans/0/fuzzable-requests/'),
                               body=FR_LIST_RESPONSE,
                               content_type='application/json')

        conn = Connection(self.api_url)

        scan = Scan(conn, scan_id=0)
        frs = scan.get_fuzzable_requests()

        self.assertEqual(frs, EXPECTED_FRS)

