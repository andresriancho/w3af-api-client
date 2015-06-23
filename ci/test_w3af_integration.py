import unittest
import os
import subprocess
import re
import time
import pprint

from w3af_api_client import Connection, Scan


class TestW3afIntegration(unittest.TestCase):

    def test_integration(self):
        """
        The main goal of this test is to assert that the latest version of w3af
        can be consumed using the latest version of w3af-api-client.
        """
        raise NotImplementedError