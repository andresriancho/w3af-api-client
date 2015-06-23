import os
import requests
import logging
import json
import urllib

from w3af_api_client import __VERSION__
from w3af_api_client.utils.exceptions import APIException

api_logger = logging.getLogger(__name__)


class Scan(object):

    def __init__(self, conn, scan_profile, target_urls):
        self.conn = conn
        self.scan_profile = scan_profile
        self.target_urls = target_urls

    def start(self):
        raise NotImplementedError

    def pause(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def cleanup(self):
        raise NotImplementedError

    def get_log(self):
        raise NotImplementedError

    def get_findings(self):
        raise NotImplementedError