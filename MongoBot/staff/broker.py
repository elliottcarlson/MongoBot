# -*- coding: utf-8 -*-
import logging
import re

from MongoBot.staff.browser import Browser
from collections import OrderedDict

logger = logging.getLogger(__name__)


# For all your stock needs
class Broker(object):

    def __init__(self, symbol):

        self.stock = None
        self.symbol = symbol
        self.price = 0

        if not symbol:
            return

        # Yahoo uses hyphens in the symbols; old portfolios might be saved with
        # dots from when we were using the Google API - look up with hyphen.
        symbol = symbol.replace('.', '-')

        # yahoo fields
        # See http://www.gummy-stuff.org/Yahoo-data.htm for more
        fields = OrderedDict([
            ('symbol', 's'),
            ('price', 'l1'),
            ('perc_change', 'p2'),
            ('change', 'c1'),
            ('exchange', 'x'),
            ('company', 'n'),
            ('volume', 'v'),
            ('market_cap', 'j1'),
        ])

        # yahoo specific
        url = 'http://download.finance.yahoo.com/d/quotes.csv'
        params = {'f': ''.join(fields.values()), 's': symbol, 'e': '.csv'}

        try:
            raw_string = Browser(url, params).read()
            raw_list = raw_string.strip().replace('"', '').split(',')
            data = {key: raw_list.pop(0) for (key) in fields.keys()}
        except Exception as e:
            logger.exception(e)
            return

        if data['exchange'] == 'N/A':
            return

        # Turn N/A - <b>92.73</b> into just the decimal
        data['price'] = float(re.search('(\d|\.)+',
                              data['price'].split('-').pop()).group())
        # Turn N/A - +0.84% into just the decimal
        data['perc_change'] = float(re.search('(\+|-)?(\d|\.)+',
                                    data['perc_change'].split('-').pop()).group())
        data['change'] = float(data['change'])

        for key, value in data.items():
            setattr(self, key, value)

        self.stock = data

    def __bool__(self):
        return self.__nonzero__()

    def __nonzero__(self):
        return self.stock is not None

    def showquote(self):

        if not self.stock:
            return False

        name = "%s (%s)" % (self.company, self.symbol.upper())
        changestring = str(self.change) + " (" + ("%.2f" % self.perc_change) + "%)"

        if self.change < 0:
            changestring = '${red:%s}' % changestring # self.colorize(changestring, 'red')
        else:
            changestring = '${green:%s}' % changestring # self.colorize(changestring, 'lightgreen')

        message = [
            name,
            str(self.price),
            changestring,
        ]

        link = 'http://finance.yahoo.com/q?s=' + self.symbol
        roasted = Browser.shorten(link)
        message.append(roasted)

        output = ', '.join(message)

        return output
