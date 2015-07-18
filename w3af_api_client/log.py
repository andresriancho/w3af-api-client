import json

from w3af_api_client.utils.exceptions import APIException


class LogEntry(object):
    def __init__(self, _type, message, _time, severity, _id):
        self.type = _type
        self.message = message
        self.time = _time
        self.severity = severity
        self.id = _id

    def __eq__(self, other):
        return (self.type == other.type and
                self.message == other.message and
                self.time == other.time and
                self.severity == other.severity and
                self.id == other.id)

    @classmethod
    def from_entry_dict(cls, entry_dict):
        """
        This is a "constructor" for the LogEntry class.

        :param entry_dict: A dict we get from the REST API
        :return: An instance of LogEntry.
        """
        # Debug helper
        # https://circleci.com/gh/andresriancho/w3af-api-docker/30
        try:
            _type = entry_dict['type']
            _id = entry_dict['id']
            _time = entry_dict['time']
            message = entry_dict['message']
            severity = entry_dict['severity']
        except KeyError:
            msg = ('Missing expected log entry attribute. Log entry'
                   ' object is:\n\n%s')
            raise APIException(msg % json.dumps(entry_dict, indent=4))

        return cls(_type, message, _time, severity, _id)


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

    def get_by_start_id(self, start_id):
        """
        :yield: Log entries starting from :start_id: and ending 200 entries
                after. In most cases easier to call than the paginate one
                because there is no need to keep track of the already read
                entries in a specific page.
        """
        url = '/scans/%s/log?id=%s' % (self.scan_id, start_id)
        code, page = self.conn.send_request(url, method='GET')

        if code != 200:
            message = page.get('message', 'None')
            args = (code, message)
            raise APIException('Failed to retrieve scan log. Received HTTP'
                               ' response code %s. Message: "%s"' % args)

        entries = page.get('entries', None)

        if entries is None:
            raise APIException('Could not retrieve log entries attribute')

        for entry_dict in entries:
            yield LogEntry.from_entry_dict(entry_dict)

    def get_page(self, page_number):
        """
        :yield: Log entries for the given page number
        """
        url = '/scans/%s/log?page=%s' % (self.scan_id, page_number)
        code, page = self.conn.send_request(url, method='GET')

        if code != 200:
            message = page.get('message', 'None')
            args = (code, message)
            raise APIException('Failed to retrieve scan log. Received HTTP'
                               ' response code %s. Message: "%s"' % args)

        entries = page.get('entries', None)

        if entries is None:
            raise APIException('Could not retrieve log entries attribute')

        for entry_dict in entries:
            yield LogEntry.from_entry_dict(entry_dict)

    def __repr__(self):
        return '<Log manager for scan ID "%s">' % self.scan_id


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