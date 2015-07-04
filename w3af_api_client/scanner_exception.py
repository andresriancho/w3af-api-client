from w3af_api_client.utils.details import Details


class ScannerException(Details):
    """
    A wrapper around the w3af scanner exception, initially it's a shallow object
    but when one of the attributes is accessed it will connect to the REST API
    and retrieve the information
    """
    def __init__(self, conn, exception_href):
        super(ScannerException, self).__init__(conn, exception_href)
