from w3af_api_client.utils.exceptions import APIException


class Details(object):
    """
    A base class that holds the details for a resource in a cached and easy
    to access way.
    """
    def __init__(self, conn, resource_href):
        self.conn = conn
        self.resource_href = resource_href
        self._data = None

    def get_data(self):
        return self._data

    def __eq__(self, other):
        return self.get_data() == other.get_data()

    def __getattr__(self, attribute_name):
        """
        :param attribute_name: The name of the attribute to access
        :return: The value of that attribute according to the REST API
        """
        try:
            return self.resource_data[attribute_name]
        except KeyError:
            # This will raise a KeyError, but we want an attribute error to
            # keep the expected "protocol" when doing instance.attribute
            msg = "Resource detail has no attribute '%s'"
            raise AttributeError(msg % attribute_name)

    @property
    def resource_data(self):
        """
        Cached access to the KB so a piece of code that accesses this finding
        doesn't perform one HTTP request to the REST API for each attribute

        :return: The JSON data
        """
        if self._data is not None:
            return self._data

        return self.update()

    def update(self):
        code, data = self.conn.send_request(self.resource_href, method='GET')

        if code != 200:
            msg = 'Could not retrieve resource detail "%s"'
            raise APIException(msg % self.resource_href)

        self._data = data
        return self._data