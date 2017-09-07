# -*- coding: utf-8 -*-
import logging
import os
import random
import re

from MongoBot.hyperthymesia import load_config
from MongoBot.staff.browser import Browser
from wordnik import swagger, WordApi

logger = logging.getLogger(__name__)


class Oracle(object):
    """
    The Oracle reaches out to the beyond to find the answers you are looking
    for.
    """

    def __init__(self, search=None):
        self.config = load_config('config/staff.yaml').get('researcher')
        self.search = search

    def etymology(self, index=0):
        word = self.search or self.get_random_word()
        res = self.query_etymonline(word)

        try:
            text = res[index]
        except IndexError:
            text = res[0]

        return 'Etymology for ${bold:%s} %s' % (text[0], text[1])

    def define(self, index=0):
        word = self.search or self.get_random_word()

        try:
            client = swagger.ApiClient(
                self.config.get('wordnik_api_key'),
                self.config.get('wordnik_api_url')
            )
        except:
            raise Exception('Unable to initialize Wordnik API.')

        api = WordApi.WordApi(client)
        res = api.getDefinitions(word)

        if not res:
            return str(NoResultsFound(word))

        try:
            return res[index].text
        except IndexError:
            return res[0].text

        return res

    def google(self):
        word = self.search or self.get_random_word()
        key = self.config.get('google_search_key')
        gid = self.config.get('google_search_id')

        params = {
            'key': key,
            'cx': gid,
            'fields': 'items(title,link)',
            'q': word
        }

        try:
            request = Browser(
                'https://www.googleapis.com/customsearch/v1',
                params=params)

            if request.error:
                return request.error

            json = request.json()

        except Exception as e:
            return 'Something\'s buggered up: %s' % str(e)

        try:
            if len(json['items']) == 0:
                return 'No results'
        except:
            return 'Non-standard response: https://www.google.com/#q=%s' % word

        result = json["items"][0]
        title = result["title"]
        link = result["link"]

        return "%s @ %s" % (title, link)

    def weather(self):
        if not self.secrets.weather_api:
            return "wunderground api key is not set"

        if not self.values:
            params = "autoip.json?geo_ip=%s" % self.lastip
        else:
            params = "%s.json" % self.values[0]

        base = "http://api.wunderground.com/api/%s/conditions/q/" % self.secrets.weather_api

        url = base + params

        try:
            request = Browser(url)
        except:
            return "Couldn't get weather."

        if not request:
            return "Couldn't get weather."

        try:
            json = request.json()
            json = json['current_observation']
        except:
            return "Couldn't parse weather."

        location = json['display_location']['full']
        condition = json['weather']
        temp = json['temperature_string']
        humid = json['relative_humidity']
        wind = json['wind_string']
        feels = json['feelslike_string']
        hourly = 'http://www.weather.com/weather/hourbyhour/l/%s' % self.values[0]
        radar = shorten('http://www.weather.com/weather/map/interactive/l/%s' % self.values[0])

        base = "%s, %s, %s, Humidity: %s, Wind: %s, Feels like: %s, Radar: %s"
        return base % (location, condition, temp, humid, wind, feels, radar)

    def get_random_word(self):
        words_file = self.config.get('words', '/usr/share/dict/words')
        if not os.path.exists(words_file):
            logger.exception(OSError(2, 'Unable to open word file!'))
            return 'mongo'

        word = random.choice(open(words_file).readlines()).rstrip('\n')
        return word

    def query_etymonline(self, word):
        soup = Browser('http://www.etymonline.com/index.php', {
            'search': word
        }).soup()

        try:
            # No-Op to test for content
            soup.dt.a.text
        except:
            raise NoResultsFound(word)

        search = {'class': 'highlight'}
        hits = [x.a.text for x in soup.findAll('dt', search)]
        etys = [self.ety_clean(x) for x in soup.findAll('dd', search)]

        results = list(zip(hits, etys))
        return results

    def ety_clean(self, soup):
        output = str()
        for i in soup:
            if i.string:
                if '<span class="foreign">' in str(i):
                    i.string = re.sub(
                        r'<span class="foreign">(.+)</span>',
                        r'${bold:\1}',
                        str(i)
                    )
                output += ' ' + i.string
            elif i.text:
                for br in i.find_all('br'):
                    br.replace_with(' ')
                output += ' ' + i.text
        output = re.sub('^\s+', '', output)
        output = re.sub('\s{2,}', ' ', output)
        output = re.sub('\s+([,)\].;:])', '\g<1>', output)
        output = re.sub('([(])\s+', '\g<1>', output)

        return output


class NoResultsFound(Exception):
    def __init__(self, value):
        self.value = 'Found no hits for query \'%s\'.' % value

    def __str__(self):
        return repr(self.value)
