import re
import sys

old_stdout = sys.stdout


class CleanUpWrapper(object):
    """
    This is a simple cleaner that will remove the user authentication
    credentials from the output, so it's safe for them to send me their verbose
    logs without sending the basic auth b64 encoded string.
    """
    def write(self, data):
        data = re.sub('Authorization: (.*?)\\\\r',
                      'Authorization: <sanitized>\\\\r',
                      data)
        old_stdout.write(data)

    def flush(self):
        old_stdout.flush()


sys.stdout = CleanUpWrapper()
