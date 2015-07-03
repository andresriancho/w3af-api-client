import logging
import time

from w3af_api_client.log import Log
from w3af_api_client.finding import Finding
from w3af_api_client.utils.exceptions import (APIException,
                                              ScanStopTimeoutException)


api_logger = logging.getLogger(__name__)


class Scan(object):

    def __init__(self, conn, scan_id=None, status=None):
        self.conn = conn
        self.scan_id = scan_id
        self.status = status

    def start(self, scan_profile, target_urls):
        data = {'scan_profile': scan_profile,
                'target_urls': target_urls}
        code, data = self.conn.send_request('/scans/',
                                            json_data=data,
                                            method='POST')

        if code != 201:
            raise APIException('Failed to start the new scan')

        api_logger.debug('Scan successfully started using REST API')
        self.scan_id = data['id']

    def get_status(self):
        assert self.scan_id is not None, 'No scan_id has been set'

        code, data = self.conn.send_request('/scans/%s/status' % self.scan_id,
                                            method='GET')

        if code != 200:
            raise APIException('Failed to retrieve scan status. Received HTTP'
                               ' response code %s' % code)

        return data

    def pause(self):
        assert self.scan_id is not None, 'No scan_id has been set'
        self.conn.send_request('/scans/%s/pause' % self.scan_id, method='GET')

    def stop(self, timeout=None):
        """
        Send the GET request required to stop the scan

        If timeout is not specified we just send the request and return. When
        it is the method will wait for (at most) :timeout: seconds until the
        scan changes it's status/stops. If the timeout is reached then an
        exception is raised.

        :param timeout: The timeout in seconds
        :return: None, an exception is raised if the timeout is exceeded
        """
        assert self.scan_id is not None, 'No scan_id has been set'

        #
        #   Simple stop
        #
        if timeout is None:
            url = '/scans/%s/stop' % self.scan_id
            self.conn.send_request(url, method='GET')
            return

        #
        #   Stop with timeout
        #
        self.stop()

        for _ in xrange(timeout):
            time.sleep(1)

            is_running = self.get_status()['is_running']
            if not is_running:
                return

        msg = 'Failed to stop the scan in %s seconds'
        raise ScanStopTimeoutException(msg % timeout)

    def cleanup(self):
        assert self.scan_id is not None, 'No scan_id has been set'
        self.conn.send_request('/scans/%s' % self.scan_id, method='DELETE')

    def get_log(self):
        assert self.scan_id is not None, 'No scan_id has been set'
        return Log(conn=self.conn, scan_id=self.scan_id)

    def get_findings(self):
        code, data = self.conn.send_request('/scans/%s/kb/' % self.scan_id,
                                            method='GET')

        if code != 200:
            raise APIException('Failed to retrieve findings')

        findings = data.get('items', None)

        if findings is None:
            raise APIException('Failed to retrieve findings')

        return [Finding(self.conn, f['href']) for f in findings]