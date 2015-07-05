import json
import httpretty

from w3af_api_client import Connection, Scan
from w3af_api_client.tests.base import BaseAPITest
from w3af_api_client.tests.test_scan import INDEX_RESPONSE, VERSION_RESPONSE


EXCEPTION_LIST_RESPONSE = json.dumps({'items': [{'id': 0,
                                                 'href': '/scans/0/exceptions/0',
                                                 'function_name': 'function',
                                                 'lineno': 112,
                                                 'exception': 'ValueError',
                                                 'plugin': 'web_spider',
                                                 'phase': 'crawl'},

                                                {'id': 1,
                                                 'href': '/scans/0/exceptions/1',
                                                 'function_name': 'f_xyz',
                                                 'lineno': 331,
                                                 'exception': 'IndexError',
                                                 'plugin': 'web_spider',
                                                 'phase': 'crawl'}]})

EXCEPTION_DETAIL_0 = json.dumps({'id': 0,
                                 'href': '/scans/0/exceptions/0',
                                 'function_name': 'function',
                                 'lineno': 112,
                                 'traceback': 'Long string with tb',
                                 'exception': 'ValueError',
                                 'plugin': 'web_spider',
                                 'phase': 'crawl'})


EXCEPTION_DETAIL_1 = json.dumps({'id': 1,
                                 'href': '/scans/0/exceptions/1',
                                 'function_name': 'f_xyz',
                                 'lineno': 331,
                                 'traceback': 'Long string with tb',
                                 'exception': 'IndexError',
                                 'plugin': 'web_spider',
                                 'phase': 'crawl'})


class TestExceptionListClient(BaseAPITest):

    @httpretty.activate
    def test_exception_list(self):
        httpretty.register_uri(httpretty.GET,
                               self.get_url('/'),
                               body=INDEX_RESPONSE,
                               content_type='application/json')

        httpretty.register_uri(httpretty.GET,
                               self.get_url('/version'),
                               body=VERSION_RESPONSE,
                               content_type='application/json')

        httpretty.register_uri(httpretty.GET,
                               self.get_url('/scans/0/exceptions/'),
                               body=EXCEPTION_LIST_RESPONSE,
                               content_type='application/json')

        httpretty.register_uri(httpretty.GET,
                               self.get_url('/scans/0/exceptions/0'),
                               body=EXCEPTION_DETAIL_0,
                               content_type='application/json')

        httpretty.register_uri(httpretty.GET,
                               self.get_url('/scans/0/exceptions/1'),
                               body=EXCEPTION_DETAIL_1,
                               content_type='application/json')

        conn = Connection(self.api_url)

        scan = Scan(conn, scan_id=0)
        exceptions = scan.get_exceptions()

        exception_0 = exceptions[0]
        exception_1 = exceptions[1]

        self.assertEqual(exception_0.lineno, 112)
        self.assertEqual(exception_1.lineno, 331)

        self.assertEqual(exception_0.exception, 'ValueError')
        self.assertEqual(exception_1.exception, 'IndexError')
