import json
import unittest
import urlparse
import httpretty


from w3af_api_client.utils.exceptions import APIException
from w3af_api_client import Connection
from w3af_api_client import LogEntry, Log
from w3af_api_client import Scan
from w3af_api_client import Finding


TARGET_URL = 'http://target.example/'

INDEX_RESPONSE = json.dumps({'docs': 'http://docs.w3af.org/en/latest/api/index.html'})

SCAN_START_REQUEST = {'scan_profile': 'mock_profile',
                      'target_urls': [TARGET_URL]}
SCAN_START_RESPONSE = json.dumps({u'message': u'Success',
                                  u'href': u'/scans/0',
                                  u'id': 0})

# More fields are returned here, but I just want some to assert that the basics
# are working
SCAN_STATUS_RESPONSE = json.dumps({'is_running': True,
                                   'is_paused': False,
                                   'exception': None})

NOT_FOUND = json.dumps({'code': 404, 'message': 'Not found'})

EMPTY_LOG_RESPONSE = json.dumps({'entries': []})

LOG_RESPONSE = json.dumps({'entries': [
    {'type': 'debug',
     'message': 'one',
     'time': '23-Jun-2015 16:21',
     'severity': None},
    {'type': 'vulnerability',
     'message': 'two',
     'time': '23-Jun-2015 16:22',
     'severity': 'High'},
]})

FINDINGS_RESPONSE = json.dumps({'items': [{'id': 0}]})

FINDINGS_DETAIL_RESPONSE = json.dumps({'name': 'SQL injection'})


class TestScanUsingClient(unittest.TestCase):

    def setUp(self):
        super(TestScanUsingClient, self).setUp()
        self.api_url = 'http://127.0.0.1:5001/'

    def get_url(self, path):
        return urlparse.urljoin(self.api_url, path)

    def assertJSONEquals(self, request, expected_json):
        self.assertEqual(json.loads(request.body),
                         expected_json)

    @httpretty.activate
    def test_simple_scan(self):
        #
        # Mock all HTTP responses
        #
        httpretty.register_uri(httpretty.GET,
                               self.get_url('/'),
                               body=INDEX_RESPONSE,
                               content_type='application/json')

        httpretty.register_uri(httpretty.POST,
                               self.get_url('/scans/'),
                               body=SCAN_START_RESPONSE,
                               content_type='application/json',
                               status=201)

        httpretty.register_uri(httpretty.GET,
                               self.get_url('/scans/0/status'),
                               body=SCAN_STATUS_RESPONSE,
                               content_type='application/json')

        httpretty.register_uri(httpretty.GET,
                               self.get_url('/scans/1/status'),
                               body=NOT_FOUND,
                               content_type='application/json',
                               status=404)

        httpretty.register_uri(httpretty.GET,
                               self.get_url('/scans/0/log'),
                               responses=[
                                   httpretty.Response(body=LOG_RESPONSE,
                                                      content_type='application/json',
                                                      status=200),
                                   httpretty.Response(body=EMPTY_LOG_RESPONSE,
                                                      content_type='application/json',
                                                      status=200),
                               ])

        httpretty.register_uri(httpretty.GET,
                               self.get_url('/kb/'),
                               body=FINDINGS_RESPONSE,
                               content_type='application/json')

        httpretty.register_uri(httpretty.GET,
                               self.get_url('/kb/0'),
                               body=FINDINGS_DETAIL_RESPONSE,
                               content_type='application/json')

        conn = Connection(self.api_url)
        #conn.set_verbose(True)

        self.assertTrue(conn.can_access_api())

        #
        #   Start a scan and assert
        #
        scan = Scan(conn)
        self.assertIsNone(scan.scan_id)

        scan.start('mock_profile', [TARGET_URL])

        self.assertJSONEquals(httpretty.last_request(), SCAN_START_REQUEST)
        self.assertEqual(scan.scan_id, 0)

        #
        #   Get scan status
        #
        json_data = scan.get_status()

        self.assertEqual(json_data['is_running'], True)
        self.assertEqual(json_data['is_paused'], False)
        self.assertEqual(json_data['exception'], None)

        #
        #   Test the error handling
        #
        scan.scan_id = 1
        self.assertRaises(APIException, scan.get_status)

        scan.scan_id = 0

        #
        #   Get the log
        #
        log = scan.get_log()
        self.assertIsInstance(log, Log)

        expected_log_entries = [LogEntry('debug', 'one',
                                         '23-Jun-2015 16:21', None),
                                LogEntry('vulnerability', 'two',
                                         '23-Jun-2015 16:22', 'High')]
        received_log_entries = []

        for log_entry in log:
            self.assertIsInstance(log_entry, LogEntry)
            received_log_entries.append(log_entry)

        self.assertEqual(received_log_entries, expected_log_entries)

        #
        #   Get the vulnerabilities
        #
        findings = scan.get_findings()
        self.assertIsInstance(findings, list)
        self.assertEqual(len(findings), 1)

        finding = findings[0]
        self.assertEqual(finding.name, 'SQL injection')
        self.assertIsInstance(finding, Finding)