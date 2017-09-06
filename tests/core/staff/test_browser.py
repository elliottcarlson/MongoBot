# -*- coding: utf-8 -*-
import logging
import mock
import unittest

from MongoBot.staff.browser import Browser
from tests.mocks.requests import MockRequest

logger = logging.getLogger(__name__)


class TestBrowser(unittest.TestCase):

    @mock.patch('requests.get', side_effect=MockRequest.get)
    def test_browser_setup(self, mock_get):
        ret = Browser('http://www.example.com')
        self.assertIsInstance(ret, Browser)

    @mock.patch('requests.get', side_effect=MockRequest.get)
    def test_browser_with_auth(self, mock_get):
        Browser('http://www.example.com', {}, 'GET', 'user:pass')

        args, kwargs = mock_get.call_args
        self.assertEqual(('user', 'pass'), kwargs.get('auth'))

    @mock.patch('requests.get', side_effect=MockRequest.post)
    def test_browser_post(self, mock_post):
        ret = Browser('http://www.example.com', {}, 'POST')

        self.assertEquals(ret.url, 'http://www.example.com')

    @mock.patch('requests.get', side_effect=MockRequest.get)
    def test_browser_read(self, mock_get):
        ret = Browser('http://www.example.com')

        self.assertIn('Example Domain', ret.read())

    @mock.patch('requests.get', side_effect=MockRequest.get)
    def test_browser_soup(self, mock_get):
        ret = Browser('http://www.example.com')
        soup = ret.soup()

        self.assertEquals(soup.title.string, 'Example Domain')

    @mock.patch('requests.get', side_effect=MockRequest.get)
    def test_browser_title(self, mock_get):
        ret = Browser('http://www.example.com')

        self.assertEquals(ret.title(), 'Example Domain')

    @mock.patch('requests.get', side_effect=MockRequest.get)
    def test_browser_headers(self, mock_get):
        ret = Browser('http://www.example.com')

        self.assertEquals(
            ret.headers().get('content-type'), 'text/html; charset=utf-8'
        )

    @mock.patch('requests.get', side_effect=MockRequest.get)
    def test_browser_json(self, mock_get):
        ret = Browser(
            'https://api.twitter.com/1.1/statuses/user_timeline.json',
            {'screen_name': 'BotMongo', 'count': 2}
        )

        self.assertIn('errors', ret.json())

    @mock.patch('requests.get', side_effect=MockRequest.get)
    def test_browser_shorten(self, mock_get):
        ret = Browser.shorten('http://www.example.com/')

        self.assertEquals(ret, 'http://roa.st/es8')

    @mock.patch('requests.get', side_effect=Exception)
    def test_browser_shorten_exception(self, mock_get):
        ret = Browser.shorten('http://www.example.com')

        self.assertEquals(ret, 'http://www.example.com')
