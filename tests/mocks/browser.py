# -*- coding: utf-8 -*-
import bs4
import hashlib
import inspect
import json
import os


class MockBrowser(object):
    url = False
    ua = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 ',
          '(KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36')
    ieua = ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;',
            ' SV1)')
    text = False
    error = False

    def __init__(self, url, params={}, method='GET', userpass=False):
        stub_id = hashlib.sha1(json.dumps(
            [locals()[arg] for arg in
            inspect.getargspec(MockBrowser.__init__).args[1:]]
        )).hexdigest()

        base_path = os.path.dirname(__file__)
        stub_path = 'stubs'
        stub_file = os.path.join(base_path, stub_path, stub_id)

        try:
            with open(stub_file, 'r') as stub_content:
                self.content = stub_content.read()
        except Exception:
            print('Unable to open stub file "%s"' % stub_file)

    def soup(self):
        return bs4(self.content)

    def json(self):
        return json.loads(self.content)

    def read(self):
        return self.content

    def title(self):
        try:
            result = self.robot.title().decode('utf-8')
        except Exception as e:
            result = str(e)

        return result

    def headers(self):
        return self.response.info()

    @staticmethod
    def shorten(url):
        return 'http://roa.st/000'
