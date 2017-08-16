# -*- coding: utf-8 -*-
import functools
import hashlib
import inspect
import json
import logging
import os

from bs4 import BeautifulSoup as bs4
from MongoBot.staff.browser import Browser

logger = logging.getLogger(__name__)


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
            logger.info('Unable to open MockBrowser stub "%s".' % stub_file)

            content = Browser(url, params, method, userpass)
            if not content.error:
                with open(stub_file, 'w') as stub_content:
                    stub_content.write(content.read())
                    self.content = content.read()
                    logger.info('Created new stub file for request.')
            else:
                logger.warning('Unable to retrieve content to build stub!')
                raise Exception

    def soup(self):
        return bs4(self.content, 'html5lib')

    def json(self):
        return json.loads(self.content)

    def read(self):
        return self.content

    def title(self):
        try:
            soup = self.soup()
            result = soup.head.title.string.decode('utf-8')
        except Exception as e:
            result = str(e)

        return result

    def headers(self):
        return []

    @staticmethod
    def shorten(url):
        return 'http://roa.st/000'
