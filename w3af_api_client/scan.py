import logging

from w3af_api_client.utils.exceptions import APIException
from w3af_api_client.log import Log
from w3af_api_client.finding import Finding

api_logger = logging.getLogger(__name__)


class Scan(object):

    def __init__(self, conn, scan_id=None):
        self.conn = conn
        self.scan_id = scan_id

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
            raise APIException('Failed to retrieve scan status')

        return data

    def pause(self):
        assert self.scan_id is not None, 'No scan_id has been set'
        self.conn.send_request('/scans/%s/pause' % self.scan_id, method='GET')

    def stop(self):
        assert self.scan_id is not None, 'No scan_id has been set'
        self.conn.send_request('/scans/%s' % self.scan_id, method='GET')

    def cleanup(self):
        assert self.scan_id is not None, 'No scan_id has been set'
        self.conn.send_request('/scans/%s' % self.scan_id, method='DELETE')

    def get_log(self):
        assert self.scan_id is not None, 'No scan_id has been set'
        return Log(conn=self.conn, scan_id=self.scan_id)

    def get_findings(self):
        code, data = self.conn.send_request('/kb/', method='GET')

        if code != 200:
            raise APIException('Failed to retrieve findings')

        findings = data.get('entries', None)

        if findings is None:
            raise APIException('Failed to retrieve findings')

        return [Finding(self.conn, f['id']) for f in findings]