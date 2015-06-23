from w3af_api_client.utils.exceptions import APIException
from w3af_api_client.utils.cached_property import cached_property


class Finding(object):
    """
    A wrapper around the finding, initially it's a shallow object but when
    one of the attributes is accessed it will connect to the REST API and
    retrieve the information
    """
    def __init__(self, conn, finding_id):
        self.conn = conn
        self.finding_id = finding_id

    def __getattr__(self, attribute_name):
        """
        :param attribute_name: The name of the attribute to access
        :return: The value of that attribute according to the REST API
        """
        # Avoid recursion with cached_property
        if attribute_name == '_cache':
            raise AttributeError()

        try:
            return self.finding_data.get(attribute_name)
        except KeyError:
            # This will raise a KeyError, but we want an attribute error to
            # keep the expected "protocol" when doing instance.attribute
            msg = "'Finding' object has no attribute '%s'"
            raise AttributeError(msg % attribute_name)

    @cached_property(2)
    def finding_data(self):
        """
        Cached access to the KB so a piece of code that accesses this finding
        doesn't perform one HTTP request to the REST API for each attribute

        :return: The JSON data
        """
        code, data = self.conn.send_request('/kb/%s' % self.finding_id,
                                            method='GET')

        if code != 200:
            raise APIException('Could not retrieve finding detail')

        return data