from w3af_api_client.finding import Finding
from w3af_api_client.traffic import Traffic


class MockFinding(Finding):
    """
    A wrapper around the finding to help test w3af-api-client implementations
    """
    DATA = {'url': 'http://www.w3af.org/',
            'var': 'id',
            'response_ids': [1, 3, 5, 42],
            'vulndb_id': 3,
            'name': 'Vulnerability name',
            'desc': 'Found vulnerability in URL',
            'long_description': 'A really long description using `markdown`',
            'fix_guidance': 'Fix it by following instructions',
            'fix_effort': 30,
            'tags': ['tag1', 'tag2'],
            'wasc_ids': [89],
            'wasc_urls': [],
            'cwe_urls': [],
            'cwe_ids': [89],
            'references': ['http://www.w3af.org/'],
            'owasp_top_10_references': [],
            'plugin_name': 'sqli',
            'severity': 'High',
            'attributes': [],
            'highlight': [],
            'uniq_id': '13f6eece-49a2-4c77-93d9-5c785ec0e29d',
            'traffic_hrefs': ['/scans/0/traffic/1',
                              '/scans/0/traffic/3',
                              '/scans/0/traffic/5',
                              '/scans/0/traffic/42']}

    def __init__(self):
        super(Finding, self).__init__(None, None)

    def get_traffic(self):
        return [MockTraffic(self.conn, traffic_href) for traffic_href in self.traffic_hrefs]

    def update(self):
        return self.DATA


class MockTraffic(Traffic):
    REQUEST = ('GET http://www.w3af.org/ HTTP/1.1\r\n'
               'Host: www.w3af.org\r\n'
               '\r\n')

    RESPONSE = ('HTTP/1.1 200 Ok\r\n'
                'Content-Length: 3\r\n'
                '\r\n'
                'abc')

    def get_data(self):
        self.request = self.REQUEST
        self.response = self.RESPONSE