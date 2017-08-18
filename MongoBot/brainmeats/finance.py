# -*- coding: utf-8 -*-
import locale
import logging
import random

from collections import OrderedDict
from MongoBot.autonomic import axon, help
from MongoBot.staff.broker import Broker
from MongoBot.staff.browser import Browser

logger = logging.getLogger(__name__)


class Finance(object):

    @axon
    @help('STOCK_SYMBOL <get stock quote>')
    def q(self):
        ret = False

        try:
            stock = Broker(self.stdin)
            ret = stock.showquote()
        except Exception as e:
            logger.exception(str(e))

        if ret is not False:
            return ret

        return 'Couldn\'t find company: %s' % self.stdin

    def get_currency_price(self, name, source, dest='USD', has_gdax=False):
        """
        Retrieve the aggregated last, low and high prices of a crypto currency.
        """
        value_of = None
        if self.values:
            try:
                value_of = float(self.values[0])
            except Exception as e:
                logger.exception(str(e))
                pass

        url = 'https://www.cryptocompare.com/api/data/coinsnapshot/'
        params = {
            'fsym': source,
            'tsym': dest
        }

        request = Browser(url, params)
        if not request:
            return "Couldn't retrieve %s data." % source.upper()

        try:
            json = request.json()['Data']['AggregatedData']
        except Exception as e:
            logger.exception(str(e))
            return "Couldn't parse %s data." % source.upper()

        if self.get('to_the_moon'):
            last = random.uniform(100, 100000)
            low = random.uniform(last - 100, last)
            high = random.uniform(last, last + 100)
            gdax = None

            if has_gdax:
                gdax_val = random.uniform(last - 20, last + 20)
                gdax = self.format_currency(gdax_val)
                if value_of:
                    gdax = float(gdax_val) * float(value_of)
        else:
            try:
                last = float(json['PRICE'])
                low = float(json['LOW24HOUR'])
                high = float(json['HIGH24HOUR'])
                gdax = None
            except Exception as e:
                logger.exception(str(e))
                return 'Something went wrong...'

            if has_gdax:
                gdax = self.get_gdax_price(source, dest, value_of)

        if value_of:
            value = float(last) * float(value_of)

            if gdax:
                gdax = ", GDAX: %s" % self.format_currency(gdax)

            return 'Value of %s %s is %s%s' % (
                value_of,
                source.upper(),
                self.format_currency(value),
                gdax if gdax else ''
            )
        else:
            response = OrderedDict()
            response['Last'] = self.format_currency(last)
            response['Low'] = self.format_currency(low)
            response['High'] = self.format_currency(high)

            if gdax:
                response['GDAX'] = gdax

            prices = ', '.join(
                [': '.join([k, str(v)]) for k, v in response.items()]
            )

            return '%s, %s' % (name, prices)

    def get_gdax_price(self, source, dest='USD', value_of=None):
        """
        Retrieve the GDAX price of a specific currency.
        """
        gdax = '(No result)'
        gdax_url = 'https://api.gdax.com/products/%s-%s/ticker' % (
            source.upper(),
            dest.upper()
        )

        try:
            g_request = Browser(gdax_url)
            g_json = g_request.json()
            gdax = self.format_currency(float(g_json['price']))
            if value_of:
                gdax = float(g_json['price']) * float(value_of)
        except:
            pass

        return gdax

    def format_currency(self, price):
        """
        Format a currency appropriately, with a check if the price is under
        $0.01 to allow sub-penny display.
        """
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        if price < 0.01:
            return '$%s' % price

        return locale.currency(price, grouping=True)

    @axon
    @help("<get current Ethereum trading information>")
    def eth(self):
        return self.get_currency_price('Ethereum', 'ETH', has_gdax=True)

    @axon
    @help("<get current Ethereum Classic trading information>")
    def etc(self):
        return self.get_currency_price('Ethereum Classic', 'ETC')

    @axon
    @help("<get current Bitcoin trading information>")
    def btc(self):
        return self.get_currency_price('Bitcoin', 'BTC', has_gdax=True)

    @axon
    @help("<get current Bitcoin Cash trading information>")
    def bcc(self):
        return self.get_currency_price('Bitcoin Cash', 'BCC')

    @axon
    @help("<get current Litecoin trading information>")
    def ltc(self):
        return self.get_currency_price('Litecoin', 'LTC', has_gdax=True)

    @axon
    @help("<get current Dogecoin trading information>")
    def doge(self):
        return self.get_currency_price('Dogecoin', 'DOGE')

    @axon
    @help("<get trading info for a list of crypto currencies>")
    def c(self):
        if not self.values:
            return "Just what do you think you're doing, Dave?"

        currency = self.values.pop(0)

        try:
            return getattr(self, currency.lower())()
        except:
            return 'No such currency'

    @axon('to.?the.?moon')
    def to_the_moon(self):
        """
        Because why not fuck with people and make them believe that their
        precious cryptocurrencies are all over the place.
        """
        self.set('to_the_moon', True)
        return 'To the moooooooooon!'

    @axon('return.?to.?earth')
    def return_to_earth(self):
        """
        Nevermind - come back to reality and show the real prices.
        """
        self.set('to_the_moon', False)
        return 'Oh, fine :('
