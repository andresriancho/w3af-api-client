import base64


class Traffic(object):
    """
    A wrapper around the HTTP request and response traffic
    """
    def __init__(self, conn, traffic_href):
        self.conn = conn
        self.traffic_href = traffic_href
        self.request = None
        self.response = None

        self.get_data()

    def get_data(self):
        code, data = self.conn.send_request(self.traffic_href, method='GET')

        self.request = base64.b64decode(data['request'])
        self.response = base64.b64decode(data['response'])

    def get_request(self):
        return self.request

    def get_response(self):
        return self.response

    def __repr__(self):
        return '<Traffic for href="%s">' % self.traffic_href

    def __eq__(self, other):
        return (self.request == other.request and
                self.response == other.response)