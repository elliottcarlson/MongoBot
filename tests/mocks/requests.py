# -*- coding: utf-8 -*-
import hashlib
import json
import logging
import os

from collections import OrderedDict
from MongoBot.staff.browser import Browser

logger = logging.getLogger(__name__)


class MockResponse:
    def __init__(self, url, params={}, method='GET', auth=None, status=200):
        stub_id = hashlib.sha1(json.dumps([
            url, OrderedDict(sorted(params.items())), method, auth
        ]).encode('utf-8')).hexdigest()

        base_path = os.path.dirname(__file__)
        stub_path = 'stubs'

        stub_file = os.path.join(base_path, stub_path, stub_id)

        try:
            with open(stub_file, 'r') as stub_content:
                self.text = stub_content.read()
        except Exception:
            print('Unable to open %s' % stub_file)
            print(url)
            raise Exception

        self.status_code = status
        self.headers = {
            'cache-control': 'no-cache',
            'content-type': 'text/html; charset=utf-8'
        }

    def json(self):
        return json.loads(self.text)


class MockRequest(object):
    @staticmethod
    def get(url, params={}, headers={}, auth=None):
        return MockResponse(url, params, 'GET', auth, 200)

    @staticmethod
    def post(url, params={}, headers={}, auth=None):
        return MockResponse(url, params, 'POST', auth, 200)
