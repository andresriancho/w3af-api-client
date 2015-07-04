from w3af_api_client.utils.exceptions import APIException
from w3af_api_client.utils.cached_property import cached_property


class Details(object):
    """
    A base class that holds the details for a resource in a cached and easy
    to access way.
    """
    def __init__(self, conn, resource_href):
        self.conn = conn
        self.resource_href = resource_href

    def __getattr__(self, attribute_name):
        """
        :param attribute_name: The name of the attribute to access
        :return: The value of that attribute according to the REST API
        """
        # Avoid recursion with cached_property
        if attribute_name == '_cache':
            raise AttributeError()

        try:
            return self.resource_data.get(attribute_name)
        except KeyError:
            # This will raise a KeyError, but we want an attribute error to
            # keep the expected "protocol" when doing instance.attribute
            msg = "Resource detail has no attribute '%s'"
            raise AttributeError(msg % attribute_name)

    @cached_property(2)
    def resource_data(self):
        """
        Cached access to the KB so a piece of code that accesses this finding
        doesn't perform one HTTP request to the REST API for each attribute

        :return: The JSON data
        """
        code, data = self.conn.send_request(self.resource_href, method='GET')

        if code != 200:
            msg = 'Could not retrieve resource detail "%s"'
            raise APIException(msg % self.resource_href)

        return data
