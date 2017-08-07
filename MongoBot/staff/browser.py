# -*- coding: utf-8 -*-
import mechanize
import urllib
import json

from bs4 import BeautifulSoup as bs4


# Better browsing through technology
class Browser(object):

    url = False
    ua = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 ',
          '(KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36')
    ieua = ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;',
            ' SV1)')
    robot = mechanize.Browser()
    text = False
    error = False

    def __init__(self, url, params={}, method='GET', userpass=False):
        self.url = url

        self.robot.set_handle_equiv(True)
        self.robot.set_handle_gzip(True)
        self.robot.set_handle_redirect(True)
        self.robot.set_handle_referer(True)
        self.robot.set_handle_robots(False)
        self.robot.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),
                                      max_time=1)

        self.robot.addheaders = [
            ('User-Agent', self.ua),
            ('Accept', '*/*'),
            ('Accept-Encoding', 'gzip,deflate,sdch'),
            ('Accept-Language', 'en-US,en;q=0.8'),
            ('Cache-Control', 'max-age=0'),
            ('Connection', 'keep-alive'),
        ]

        if userpass:
            user, password = userpass.split(':')
            self.robot.add_password(url, user, password)

        # TODO params are broken
        try:
            if params:
                data = urllib.urlencode(params)
            if params and method == 'GET':
                self.response = self.robot.open(url + '?%s' % data)
            elif params and method == 'POST':
                self.response = self.robot.open(url, data)
            else:
                self.response = self.robot.open(url)

        except Exception as e:
            self.error = str(e)

    def soup(self):
        return bs4(self.response.read())

    def json(self):
        return json.loads(self.response.read())

    def read(self):
        return self.response.read()

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

        try:
            shortener = Browser('http://roa.st/api.php', params={'roast': url})
            return shortener.read()
        except:
            return url
