import unittest
import socket
import time

from w3af_api_client import Connection, Scan, Log, LogEntry, Finding
from ci.constants import FAST_TEST_PROFILE


class TestW3afIntegration(unittest.TestCase):

    W3AF_API_URL = 'http://127.0.0.1:5000/'
    TARGET_URL_FMT = 'http://%s:8000/'

    def test_integration(self):
        """
        The main goal of this test is to assert that the latest version of w3af
        can be consumed using the latest version of w3af-api-client.
        """
        conn = Connection(self.W3AF_API_URL)

        target_urls = [self.TARGET_URL_FMT % self.get_network_address()]

        scan = Scan(conn)
        scan.start(FAST_TEST_PROFILE, target_urls)

        # Wait some time for the scan to finish, these wait methods also assert
        # that I'm able to retrieve the scan status
        self.wait_until_running(scan)
        self.wait_until_finish(scan)

        log = scan.get_log()
        self.assertIsInstance(log, Log)

        log_entry_count = 0

        for log_entry in log:
            self.assertIsInstance(log_entry, LogEntry)
            self.assertIsNotNone(log_entry.message)
            log_entry_count += 1

        self.assertGreater(log_entry_count, 100)

        findings_list = scan.get_findings()
        self.assertGreaterEqual(len(findings_list), 4)

        finding = findings_list[0]
        self.assertIsInstance(finding, Finding)
        self.assertEqual(finding.name, 'SQL injection')

    def get_network_address(self):
        """
        Since the w3af scan is run inside one docker container and the target
        app is run inside ANOTHER container, I need to get the address of the
        network interface and use that as a target.

        Get the "public" IP address without sending any packets.

        :return: The IP address of the network interface
        """
        connect_target = '4.4.4.2'
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # UDP is connection-less, no packets are sent to 4.4.4.2
        # I use port 80, but could use any port
        sock.connect((connect_target, 80))
        local_address = sock.getsockname()[0]
        return local_address

    def wait_until_running(self, scan):
        """
        Wait until the scan is in Running state
        :return: The HTTP response
        """
        for _ in xrange(10):
            time.sleep(0.5)

            status = scan.get_status()
            if status['items'][0]['status'] != 'Stopped':
                return

        raise RuntimeError('Timeout waiting for scan to run')

    def wait_until_finish(self, scan, wait_loops=100):
        """
        Wait until the scan is in Stopped state
        :return: The HTTP response
        """
        for _ in xrange(wait_loops):
            time.sleep(0.5)

            status = scan.get_status()
            if status['items'][0]['status'] != 'Running':
                return

        raise RuntimeError('Timeout waiting for scan to run')