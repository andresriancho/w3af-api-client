class APIException(Exception):
    pass


class ClientException(Exception):
    pass


class ScanStopTimeoutException(Exception):
    pass


class NotFoundException(APIException):
    pass


class BadRequestException(APIException):
    pass


class ForbiddenException(APIException):
    pass