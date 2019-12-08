import json
import responses
from base import BaseAPITest
from test_scan import INDEX_RESPONSE, VERSION_RESPONSE

from w3af_api_client import Connection


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


class TestScanStopDeleteClient(BaseAPITest):

    @responses.activate
    def test_scan_list(self):
        responses.add(responses.GET,
                               self.get_url('/'),
                               body=INDEX_RESPONSE,
                               content_type='application/json')

        responses.add(responses.GET,
                               self.get_url('/version'),
                               body=VERSION_RESPONSE,
                               content_type='application/json')
        
        responses.add(responses.GET,
                               self.get_url('/scans/'),
                               body=SCAN_LIST_RESPONSE,
                               content_type='application/json')

        responses.add(responses.DELETE,
                               self.get_url('/scans/1'),
                               body=SCAN_LIST_RESPONSE,
                               content_type='application/json')

        responses.add(responses.GET,
                               self.get_url('/scans/0/stop'),
                               body=SCAN_LIST_RESPONSE,
                               content_type='application/json')

        conn = Connection(self.api_url)

        scans = conn.get_scans()
        running_scan = scans[0]
        stopped_scan = scans[1]

        running_scan.stop()
        self.assertEqual(responses.calls[-1].request.path_url, '/scans/0/stop')

        stopped_scan.cleanup()
        self.assertEqual(responses.calls[-1].request.path_url, '/scans/1')
        self.assertEqual(responses.calls[-1].request.method, 'DELETE')

