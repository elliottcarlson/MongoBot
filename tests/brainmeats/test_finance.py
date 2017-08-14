import mock
import sys
import unittest

from MongoBot.brainmeats.finance import Finance
from tests.mocks.broker import MockBroker
from tests.mocks.browser import MockBrowser


class TestFinance(unittest.TestCase):

    def setUp(self):
        self.finance = Finance()
        self.finance.values = []

    def test_Finance(self):
        self.assertIsInstance(self.finance, Finance)

    def test_q_has_axon(self):
        self.assertTrue(hasattr(self.finance.q, 'axon'))

    def test_q_has_help(self):
        self.assertTrue(hasattr(self.finance.q, 'help'))
        self.assertEquals(self.finance.q.help, 'STOCK_SYMBOL <get stock quote>')

    @mock.patch('MongoBot.brainmeats.finance.Broker', new=MockBroker)
    def test_q_valid_quote(self):
        self.finance.stdin = 'GOOG'
        ret = self.finance.q()
        self.assertEquals(
            ret,
            'Alphabet Inc. (GOOG), 914.39, ${green:7.15 (0.79%)}, http://roa.st/cok'
        )

    @mock.patch('MongoBot.brainmeats.finance.Broker', new=MockBroker)
    def test_q_invalid_quote(self):
        self.finance.stdin = 'INVALID'
        ret = self.finance.q()
        self.assertEquals(ret, 'Couldn\'t find company: INVALID')

    @mock.patch('MongoBot.brainmeats.finance.Broker', new=MockBroker)
    def test_q_no_quote(self):
        self.finance.stdin = None
        ret = self.finance.q()
        self.assertEquals(ret, 'Couldn\'t find company: None')

    @mock.patch('logging.Logger.exception')
    @mock.patch('MongoBot.brainmeats.finance.Broker')
    def test_q_exception_quote(self, mocked_broker, mocked_logger):
        self.finance.stdin = None
        mocked_broker.return_value = lambda: ().throw(Exception(None))
        ret = self.finance.q()
        mocked_logger.assert_called_with('\'function\' object has no attribute \'showquote\'')

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_get_currency_price_with_gdax(self):
        name = 'Bitcoin'
        source = 'BTC'
        dest = 'USD'
        has_gdax = True

        ret = self.finance.get_currency_price(name, source, dest, has_gdax)

        self.assertEquals(
            ret,
            'Bitcoin, Last: $4,047.10, Low: $3,841.92, High: $4,200.93, GDAX: $4,294.96'
        )

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_get_currency_price_value_via_int_with_gdax(self):
        self.finance.values = [300]

        name = 'Bitcoin'
        source = 'BTC'
        dest = 'USD'
        has_gdax = True

        ret = self.finance.get_currency_price(name, source, dest, has_gdax)

        self.assertEquals(
            ret,
            'Value of 300.0 BTC is $1,214,130.00, GDAX: $1,288,488.00'
        )

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_get_currency_price_value_via_float_with_gdax(self):
        self.finance.values = [2.5]

        name = 'Bitcoin'
        source = 'BTC'
        dest = 'USD'
        has_gdax = True

        ret = self.finance.get_currency_price(name, source, dest, has_gdax)

        self.assertEquals(
            ret,
            'Value of 2.5 BTC is $10,117.75, GDAX: $10,737.40'
        )

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_get_currency_price_without_gdax(self):
        name = 'Bitcoin'
        source = 'BTC'
        dest = 'USD'
        has_gdax = False

        ret = self.finance.get_currency_price(name, source, dest, has_gdax)

        self.assertEquals(
            ret,
            'Bitcoin, Last: $4,047.10, Low: $3,841.92, High: $4,200.93'
        )

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_get_currency_price_value_via_int_without_gdax(self):
        self.finance.values = [300]

        name = 'Bitcoin'
        source = 'BTC'
        dest = 'USD'
        has_gdax = False

        ret = self.finance.get_currency_price(name, source, dest, has_gdax)

        self.assertEquals(
            ret,
            'Value of 300.0 BTC is $1,214,130.00'
        )

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_get_currency_price_value_via_float_without_gdax(self):
        self.finance.values = [2.5]

        name = 'Bitcoin'
        source = 'BTC'
        dest = 'USD'
        has_gdax = False

        ret = self.finance.get_currency_price(name, source, dest, has_gdax)

        self.assertEquals(
            ret,
            'Value of 2.5 BTC is $10,117.75'
        )

    @mock.patch('logging.Logger.exception')
    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_get_currency_price_value_with_invalid_value(self, mocked_logger):
        self.finance.values = ['invalid']

        name = 'Bitcoin'
        source = 'BTC'
        dest = 'USD'
        has_gdax = True

        ret = self.finance.get_currency_price(name, source, dest, has_gdax)

        mocked_logger.assert_called_with('could not convert string to float: invalid')
        self.assertEquals(
            ret,
            'Bitcoin, Last: $4,047.10, Low: $3,841.92, High: $4,200.93, GDAX: $4,294.96'
        )

    @mock.patch('MongoBot.brainmeats.finance.Browser')
    def test_get_currency_price_empty_browser_response(self, mocked_browser):
        name = 'Bitcoin'
        source = 'BTC'
        dest = 'USD'
        has_gdax = False

        mocked_browser.return_value = False

        ret = self.finance.get_currency_price(name, source, dest, has_gdax)

        self.assertEquals(ret, 'Couldn\'t retrieve BTC data.')

    @mock.patch('logging.Logger.exception')
    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_get_currency_price_unexpected_json_response(self, mocked_logger):
        name = 'Litecoin'
        source = 'LTC'
        dest = 'EUR'
        has_gdax = False

        ret = self.finance.get_currency_price(name, source, dest, has_gdax)

        mocked_logger.assert_called_with('\'Data\'')
        self.assertEquals(ret, 'Couldn\'t parse LTC data.')

    @mock.patch('logging.Logger.exception')
    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_get_currency_price_value_invalid_response_price(self, mocked_logger):
        self.finance.values = [2.5]

        name = 'Ethereum'
        source = 'ETH'
        dest = 'EUR'
        has_gdax = False

        ret = self.finance.get_currency_price(name, source, dest, has_gdax)

        mocked_logger.assert_called_with('could not convert string to float: XXX')
        self.assertEquals(ret, 'Something went wrong...')

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_get_gdax_price_with_value(self):
        source = 'BTC'
        dest = 'USD'
        value = '300'

        ret = self.finance.get_gdax_price(source, dest, value)

        self.assertEquals(ret, 1288488.0)

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_get_gdax_price_without_value(self):
        source = 'BTC'
        dest = 'USD'
        value = None

        ret = self.finance.get_gdax_price(source, dest, value)

        self.assertEquals(ret, '$4,294.96')

    @mock.patch('MongoBot.brainmeats.finance.Browser')
    def test_get_gdax_price_with_exception(self, mocked_browser):
        source = 'BTC'
        dest = 'USD'
        value = 'XXX'

        mocked_browser.return_value = False

        ret = self.finance.get_gdax_price(source, dest, value)

        self.assertEquals(ret, '(No result)')

    def test_format_currency(self):
        price = 34567.123

        ret = self.finance.format_currency(price)

        self.assertEquals(ret, '$34,567.12')

    def test_format_currency_sub_penny(self):
        price = 0.0012345

        ret = self.finance.format_currency(price)

        self.assertEquals(ret, '$0.0012345')

    def test_eth_has_axon(self):
        self.assertTrue(hasattr(self.finance.eth, 'axon'))

    def test_eth_has_help(self):
        self.assertTrue(hasattr(self.finance.eth, 'help'))
        self.assertEquals(
            self.finance.eth.help,
            '<get current Ethereum trading information>'
        )

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_eth_for_price(self):
        ret = self.finance.eth()
        self.assertEquals(
            ret,
            'Ethereum, Last: $298.78, Low: $292.04, High: $307.10, GDAX: $299.80'
        )

    def test_etc_has_axon(self):
        self.assertTrue(hasattr(self.finance.etc, 'axon'))

    def test_etc_has_help(self):
        self.assertTrue(hasattr(self.finance.etc, 'help'))
        self.assertEquals(
            self.finance.etc.help,
            '<get current Ethereum Classic trading information>'
        )

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_etc_for_price(self):
        ret = self.finance.etc()
        self.assertEquals(
            ret,
            'Ethereum Classic, Last: $13.92, Low: $13.74, High: $14.56'
        )

    def test_btc_has_axon(self):
        self.assertTrue(hasattr(self.finance.btc, 'axon'))

    def test_btc_has_help(self):
        self.assertTrue(hasattr(self.finance.btc, 'help'))
        self.assertEquals(
            self.finance.btc.help,
            '<get current Bitcoin trading information>'
        )

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_btc_for_price(self):
        ret = self.finance.btc()
        self.assertEquals(
            ret,
            'Bitcoin, Last: $4,047.10, Low: $3,841.92, High: $4,200.93, GDAX: $4,294.96'
        )

    def test_bcc_has_axon(self):
        self.assertTrue(hasattr(self.finance.bcc, 'axon'))

    def test_bcc_has_help(self):
        self.assertTrue(hasattr(self.finance.bcc, 'help'))
        self.assertEquals(
            self.finance.bcc.help,
            '<get current Bitcoin Cash trading information>'
        )

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_bcc_for_price(self):
        ret = self.finance.bcc()
        self.assertEquals(
            ret,
            'Bitcoin Cash, Last: $3,600.00, Low: $3,277.00, High: $3,600.00'
        )

    def test_ltc_has_axon(self):
        self.assertTrue(hasattr(self.finance.ltc, 'axon'))

    def test_ltc_has_help(self):
        self.assertTrue(hasattr(self.finance.ltc, 'help'))
        self.assertEquals(
            self.finance.ltc.help,
            '<get current Litecoin trading information>'
        )

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_ltc_for_price(self):
        ret = self.finance.ltc()
        self.assertEquals(
            ret,
            'Litecoin, Last: $45.43, Low: $44.92, High: $46.52, GDAX: $45.32' 
        )

    def test_doge_has_axon(self):
        self.assertTrue(hasattr(self.finance.doge, 'axon'))

    def test_doge_has_help(self):
        self.assertTrue(hasattr(self.finance.doge, 'help'))
        self.assertEquals(
            self.finance.doge.help,
            '<get current Dogecoin trading information>'
        )

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_doge_for_price(self):
        ret = self.finance.doge()
        self.assertEquals(
            ret,
            'Dogecoin, Last: $0.001722, Low: $0.001681, High: $0.001871'
        )

    def test_c_has_axon(self):
        self.assertTrue(hasattr(self.finance.c, 'axon'))

    def test_c_has_help(self):
        self.assertTrue(hasattr(self.finance.c, 'help'))
        self.assertEquals(
            self.finance.c.help,
            '<get trading info for a list of crypto currencies>'
        )

    def test_c_without_values(self):
        ret = self.finance.c()

        self.assertEquals(
            ret,
            'Just what do you think you\'re doing, Dave?'
        )

    #@mock.patch('logging.Logger.
    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_c_with_valid_currency(self):
        self.finance.values = ['BTC']

        ret = self.finance.c()

        self.assertEquals(
            ret,
            'Bitcoin, Last: $4,047.10, Low: $3,841.92, High: $4,200.93, GDAX: $4,294.96'
        )

    def test_c_with_invalid_currenct(self):
        self.finance.values = ['INVALID']

        ret = self.finance.c()

        self.assertEquals(
            ret,
            'No such currency'
        )
