import json
import httpretty

from w3af_api_client import Connection
from w3af_api_client import LogEntry, Log
from w3af_api_client import Scan
from w3af_api_client.tests.base import BaseAPITest
from w3af_api_client.tests.test_scan import (INDEX_RESPONSE,
                                             VERSION_RESPONSE,
                                             SCAN_START_RESPONSE,
                                             TARGET_URL)

EMPTY_LOG_RESPONSE = json.dumps({'entries': []})

LOG_RESPONSE = json.dumps({'entries': [
    {'type': 'debug',
     'message': 'one',
     'time': '23-Jun-2015 16:21',
     'severity': None,
     'id': 0},
    {'type': 'vulnerability',
     'message': 'two',
     'time': '23-Jun-2015 16:22',
     'severity': 'High',
     'id': 1},
]})


class TestLogAccess(BaseAPITest):

    @httpretty.activate
    def test_log_access(self):
        #
        # Mock all HTTP responses
        #
        httpretty.register_uri(httpretty.GET,
                               self.get_url('/'),
                               body=INDEX_RESPONSE,
                               content_type='application/json')

        httpretty.register_uri(httpretty.GET,
                               self.get_url('/version'),
                               body=VERSION_RESPONSE,
                               content_type='application/json')

        httpretty.register_uri(httpretty.POST,
                               self.get_url('/scans/'),
                               body=SCAN_START_RESPONSE,
                               content_type='application/json',
                               status=201)

        httpretty.register_uri(httpretty.GET,
                               self.get_url('/scans/0/log'),
                               responses=[
                                   #
                                   #    Responses for ?page pagination
                                   #
                                   httpretty.Response(body=LOG_RESPONSE,
                                                      content_type='application/json',
                                                      status=200),
                                   httpretty.Response(body=EMPTY_LOG_RESPONSE,
                                                      content_type='application/json',
                                                      status=200),
                                   #
                                   #    Responses for ?id=0 pagination
                                   #
                                   httpretty.Response(body=LOG_RESPONSE,
                                                      content_type='application/json',
                                                      status=200),
                                   httpretty.Response(body=EMPTY_LOG_RESPONSE,
                                                      content_type='application/json',
                                                      status=200),
                               ])


        conn = Connection(self.api_url)
        #conn.set_verbose(True)

        self.assertTrue(conn.can_access_api())

        #
        #   Start a scan and assert
        #
        scan = Scan(conn)
        self.assertIsNone(scan.scan_id)

        scan.start('mock_profile', [TARGET_URL])

        #
        #   Get the log
        #
        log = scan.get_log()
        self.assertIsInstance(log, Log)

        expected_log_entries = [LogEntry('debug', 'one',
                                         '23-Jun-2015 16:21', None, 0),
                                LogEntry('vulnerability', 'two',
                                         '23-Jun-2015 16:22', 'High', 1)]
        received_log_entries = []

        for log_entry in log:
            self.assertIsInstance(log_entry, LogEntry)
            received_log_entries.append(log_entry)

        self.assertEqual(received_log_entries, expected_log_entries)

        #
        #   Get the log using the ids
        #
        log = scan.get_log()
        self.assertIsInstance(log, Log)

        expected_log_entries = [LogEntry('debug', 'one',
                                         '23-Jun-2015 16:21', None, 0),
                                LogEntry('vulnerability', 'two',
                                         '23-Jun-2015 16:22', 'High', 1)]
        received_log_entries = []

        for log_entry in log.get_by_start_id(0):
            self.assertIsInstance(log_entry, LogEntry)
            received_log_entries.append(log_entry)

        self.assertEqual(received_log_entries, expected_log_entries)

