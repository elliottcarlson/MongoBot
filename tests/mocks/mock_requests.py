# -*- coding: utf-8 -*-
import hashlib
import json
import logging
import os

from collections import OrderedDict
from requests import Session as OGRequestSession

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
            raise Exception(stub_file)
        finally:
            stub_content.close()

        self.status_code = status
        self.headers = {
            'cache-control': 'no-cache',
            'content-type': 'text/html; charset=utf-8'
        }

    def json(self):
        return json.loads(self.text)


class MockSession(object):
    def __init__(self):
        self.params = {}

    def request(self, method, url, *args, **kwargs):
        try:
            return MockResponse(
                url,
                params=self.params,
                method=method,
                auth=None
            )
        except Exception as e:
            session = OGRequestSession()
            session.params = self.params
            resp = session.request(
                method, url, data=kwargs.get('data'), auth=kwargs.get('auth')
            )
            with open(e.message, 'w') as stub_content:
                stub_content.write(resp.text)
                logger.info('Created new stub file for request.')
            stub_content.close()
            return resp


class MockRequest(object):
    @staticmethod
    def get(url, params={}, headers={}, auth=None):
        return MockResponse(url, params, 'GET', auth, 200)

    @staticmethod
    def post(url, params={}, headers={}, auth=None):
        return MockResponse(url, params, 'POST', auth, 200)

    @staticmethod
    def Session():
        return MockSession()
