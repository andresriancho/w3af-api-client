import requests
import urlparse
import logging
import json

# These two lines enable debugging at httplib level
# (requests->urllib3->http.client) You will see the REQUEST, including HEADERS
# and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client


from w3af_api_client import __VERSION__
from w3af_api_client.utils.exceptions import APIException
from w3af_api_client.utils.constants import ISSUE_URL

api_logger = logging.getLogger(__name__)


class Connection(object):

    def __init__(self, api_url, verbose=False):
        self.api_url = api_url
        self.session = None

        self.set_verbose(verbose)
        self.configure_requests()
        self.can_access_api()

    def can_access_api(self):
        """
        :return: True when we can access the REST API
        """
        try:
            code, _ = self.send_request(self.api_url)
        except Exception, e:
            msg = 'An exception was raised when connecting to REST API: "%s"'
            raise APIException(msg % e)
        else:
            if code in (200, 404):
                return True

            msg = 'Unexpected HTTP response code %s when connecting to REST API'
            raise APIException(msg % code)

    def set_verbose(self, verbose):
        # Get level based on verbose boolean
        level = logging.DEBUG if verbose else logging.CRITICAL

        # Configure my own logger
        api_logger.setLevel(level=level)

        ch = logging.StreamHandler()
        ch.setLevel(level)

        formatter = logging.Formatter('%(message)s')
        ch.setFormatter(formatter)
        api_logger.addHandler(ch)

        # Configure the loggers for urllib3, requests and httplib
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(level)
        requests_log.propagate = True

        requests_log = logging.getLogger("requests")
        requests_log.setLevel(level)

        http_client.HTTPConnection.debuglevel = 1 if verbose else 0

    def configure_requests(self):
        self.session = requests.Session()

        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'User-Agent': 'REST API Client %s' % __VERSION__}
        self.session.headers.update(headers)

    def send_request(self, path, json_data=None, method='GET'):
        full_url = urlparse.urljoin(self.api_url, path)

        if method == 'GET':
            response = self.session.get(full_url)

        elif method == 'DELETE':
            response = self.session.delete(full_url)

        elif method == 'POST':
            data = json.dumps(json_data)
            response = self.session.post(full_url, data=data)

        else:
            raise ValueError('Invalid HTTP method: "%s"' % method)

        try:
            json_data = response.json()
        except ValueError:
            msg = ('REST API service did not return JSON, if this issue'
                   ' persists please create an issue in the w3af framework'
                   ' repository at %s')
            raise APIException(msg % ISSUE_URL)

        pretty_json = json.dumps(json_data, indent=4)
        msg = 'Received %s HTTP response from the wire:\n%s'
        api_logger.debug(msg % (response.status_code, pretty_json))

        #
        # Error handling
        #
        if response.status_code in (400, 403, 404):
            error = json_data.get('error', None)
            if error is not None:
                raise APIException(error)
            else:
                msg = ('REST API service did not return the expected "error"'
                       ' attribute for the %s response. Please create a new'
                       ' issue in the w3af framework repository at %s')
                raise APIException(msg % (response.status_code, ISSUE_URL))

        return response.status_code, json_data
