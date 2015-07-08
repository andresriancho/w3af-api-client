__VERSION__ = '1.1.4'

try:
    from .connection import Connection
    from .finding import Finding
    from .log import Log, LogEntry
    from .scan import Scan
    from .scanner_exception import ScannerException
except ImportError:
    # https://circleci.com/gh/andresriancho/w3af-api-client/19
    pass


