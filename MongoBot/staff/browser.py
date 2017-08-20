# -*- coding: utf-8 -*-
import requests

from bs4 import BeautifulSoup as bs4


# Better browsing through technology
class Browser(object):

    url = False
    ua = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 '
          '(KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36')
    ieua = ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;'
            ' SV1)')
    text = False
    error = False

    def __init__(self, url, params={}, method='GET', userpass=False):
        self.url = url
        headers = {
            'User-Agent': self.ua,
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
        }

        auth = None
        if userpass:
            user, password = userpass.split(':')
            auth = (user, password)

        if method == 'POST':
            self.response = requests.post(
                url, data=params, headers=headers, auth=auth
            )
        else:
            self.response = requests.get(
                url, params=params, headers=headers, auth=auth
            )

    def soup(self):
        return bs4(self.response.text)

    def json(self):
        return self.response.json()

    def read(self):
        return self.response.text

    def title(self):
        soup = self.soup()
        return soup.title.string

    def headers(self):
        return self.headers

    @staticmethod
    def shorten(url):
        try:
            shortener = Browser('http://roa.st/api.php', params={'roast': url})
            return shortener.read()
        except:
            return url
