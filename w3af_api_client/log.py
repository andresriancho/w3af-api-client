from collections import namedtuple
from w3af_api_client.utils.exceptions import APIException


LogEntry = namedtuple('LogEntry', ['type', 'message', 'time', 'severity'])


class Log(object):
    """
    A wrapper around the scan log, initially it's a shallow object but when
    one of the attributes is accessed it will connect to the REST API and
    retrieve the information

    It also handles pagination, so you can iterate over the scan log without
    any effort
    """
    def __init__(self, conn, scan_id):
        self.conn = conn
        self.scan_id = scan_id

    def __iter__(self):
        return log_entry_generator(self)

    def get_page(self, page_number):
        url = '/scans/%s/log?page=%s' % (self.scan_id, page_number)
        code, page = self.conn.send_request(url, method='GET')

        if code != 200:
            raise APIException('Could not retrieve log entry list')

        entries = page.get('entries', None)

        if entries is None:
            raise APIException('Could not retrieve log entries attribute')

        for entry_dict in entries:
            yield LogEntry(entry_dict['type'],
                           entry_dict['message'],
                           entry_dict['time'],
                           entry_dict['severity'])


def log_entry_generator(log_instance):
    """
    :yield: The next LogEntry from the REST API
    :raise: StopIteration when there are no more log entries to show, please
            note that if you call this again at a later time the REST API
            could have different results and more data could be returned
    """
    current_page_num = 0

    while True:
        has_results = False

        for log_entry in log_instance.get_page(current_page_num):
            has_results = True
            yield log_entry

        if not has_results:
            break

        current_page_num += 1