# -*- coding: utf-8 -*-
import locale

from collections import OrderedDict
from MongoBot.autonomic import axon, help
from MongoBot.staff.broker import Broker
from MongoBot.staff.browser import Browser


class Finance(object):

    @axon
    # @help('STOCK_SYMBOL <get stock quote>')
    def q(self):
        ret = False

        try:
            stock = Broker(self.stdin)
            ret = stock.showquote()
        except Exception as e:
            pass

        if not ret:
            ret = 'Couldn\'t find company: %s' % self.stdin

        return ret

    def get_currency_price(self, name, source, dest='USD', has_gdax=False):
        """
        Retrieve the aggregated last, low and high prices of a crypto currency.
        """
        value_of = None
        if self.values:
            try:
                value_of = float(self.values[0])
            except:
                pass

        url = 'https://www.cryptocompare.com/api/data/coinsnapshot/?fsym=%s&tsym=%s'

        request = Browser(url % (source, dest))
        if not request:
            return "Couldn't retrieve %s data." % source.upper()

        try:
            json = request.json()['Data']['AggregatedData']
        except:
            return "Couldn't parse %s data." % source.upper()

        last = float(json['PRICE'])
        low = float(json['LOW24HOUR'])
        high = float(json['HIGH24HOUR'])
        gdax = None

        if has_gdax:
            gdax = self.get_gdax_price(source, dest, value_of)

        if value_of:
            try:
                value = float(json['PRICE']) * float(value_of)
            except:
                return "Couldn't compute %s value." % source.upper()

            if gdax:
                gdax = ", GDAX: %s" % self.format_currency(gdax)

            return 'Value of %s %s is %s%s' % (value_of, source.upper(), self.format_currency(value), gdax if gdax else '')
        else:
            response = OrderedDict()
            response['Last'] = self.format_currency(last)
            response['Low'] = self.format_currency(low)
            response['High'] = self.format_currency(high)

            if gdax:
                response['GDAX'] = gdax

            prices = ", ".join([": ".join([key, str(val)]) for key, val in response.items()])

            return '%s, %s' % (name, prices)

    def get_gdax_price(self, source, dest='USD', value_of=None):
        """
        Retrieve the GDAX price of a specific currency.
        """
        gdax = '(No result)'
        gdax_url = 'https://api.gdax.com/products/%s-%s/ticker' % (source.upper(), dest.upper())
        g_request = Browser(gdax_url)
        try:
            g_json = g_request.json()
            gdax = self.format_currency(float(g_json['price']))
            if value_of:
                gdax = float(g_json['price']) * float(value_of)
        except:
            pass

        return gdax

    def format_currency(self, price):
        """
        Format a currency appropriately, with a check if the price is under $0.01 to allow sub-penny display.
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

        currency = self.stdin

        try:
            return getattr(self, currency.lower())()
        except:
            return 'No such currency'
