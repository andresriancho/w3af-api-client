import unittest
import httpretty
import json


class TestScanUsingClient(unittest.TestCase):

    @httpretty.activate
    def test_simple_scan(self):
        raise NotImplementedError