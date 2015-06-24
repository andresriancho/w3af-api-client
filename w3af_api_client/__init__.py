__VERSION__ = '1.0.1'

try:
    from .connection import Connection
    from .finding import Finding
    from .log import Log, LogEntry
    from .scan import Scan
except ImportError:
    # https://circleci.com/gh/andresriancho/w3af-api-client/19
    pass


