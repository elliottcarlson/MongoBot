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

    def _should_be_axon(func):
        """
        Decorator to check that method is an axon. Only use it on a test method
        using the naming convention of test_<method to test>().

        Usage:

            @_should_be_axon
            def test_advice(self):
                ...
        """
        def check(self):
            func_name = func.__name__.split('test_', 1)[1]
            func_root = getattr(self.finance, func_name)
            self.assertTrue(hasattr(func_root, 'axon'))
            func(self)

        return check

    def test_Finance(self):
        self.assertIsInstance(self.finance, Finance)

    @mock.patch('MongoBot.brainmeats.finance.Broker', new=MockBroker)
    @_should_be_axon
    def test_q(self):
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
    def test_get_currency_price_to_the_moon(self):
        name = 'Ethereum'
        source = 'ETH'
        dest = 'EUR'
        has_gdax = False

        self.finance.to_the_moon()
        self.assertTrue(self.finance._to_the_moon)
        ret = self.finance.get_currency_price(name, source, dest, has_gdax)
        self.assertTrue(ret.startswith(name))

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_get_currency_price_to_the_moon_with_gdax(self):
        name = 'Ethereum'
        source = 'ETH'
        dest = 'EUR'
        has_gdax = True

        self.finance.to_the_moon()
        self.assertTrue(self.finance._to_the_moon)
        ret = self.finance.get_currency_price(name, source, dest, has_gdax)
        self.assertTrue(ret.startswith(name))
        self.assertTrue('GDAX' in ret)

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

    @mock.patch('MongoBot.brainmeats.finance.Browser', side_effect=Exception)
    def test_get_gdax_price_with_exception(self, mocked_browser):
        source = 'BTC'
        dest = 'USD'
        value = 'XXX'

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

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    @_should_be_axon
    def test_eth(self):
        ret = self.finance.eth()
        self.assertEquals(
            ret,
            'Ethereum, Last: $298.78, Low: $292.04, High: $307.10, GDAX: $299.80'
        )

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    @_should_be_axon
    def test_etc(self):
        ret = self.finance.etc()
        self.assertEquals(
            ret,
            'Ethereum Classic, Last: $13.92, Low: $13.74, High: $14.56'
        )

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    @_should_be_axon
    def test_btc(self):
        ret = self.finance.btc()
        self.assertEquals(
            ret,
            'Bitcoin, Last: $4,047.10, Low: $3,841.92, High: $4,200.93, GDAX: $4,294.96'
        )

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    @_should_be_axon
    def test_bcc(self):
        ret = self.finance.bcc()
        self.assertEquals(
            ret,
            'Bitcoin Cash, Last: $3,600.00, Low: $3,277.00, High: $3,600.00'
        )

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    @_should_be_axon
    def test_ltc(self):
        ret = self.finance.ltc()
        self.assertEquals(
            ret,
            'Litecoin, Last: $45.43, Low: $44.92, High: $46.52, GDAX: $45.32' 
        )

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    @_should_be_axon
    def test_doge(self):
        ret = self.finance.doge()
        self.assertEquals(
            ret,
            'Dogecoin, Last: $0.001722, Low: $0.001681, High: $0.001871'
        )

    @_should_be_axon
    def test_c(self):
        ret = self.finance.c()

        self.assertEquals(
            ret,
            'Just what do you think you\'re doing, Dave?'
        )

    @mock.patch('MongoBot.brainmeats.finance.Browser', new=MockBrowser)
    def test_c_with_valid_currency(self):
        self.finance.values = ['BTC']

        ret = self.finance.c()

        self.assertEquals(
            ret,
            'Bitcoin, Last: $4,047.10, Low: $3,841.92, High: $4,200.93, GDAX: $4,294.96'
        )

    def test_c_with_invalid_currency(self):
        self.finance.values = ['INVALID']

        ret = self.finance.c()

        self.assertEquals(
            ret,
            'No such currency'
        )

    @_should_be_axon
    def test_to_the_moon(self):
        self.assertFalse(self.finance._to_the_moon)
        ret = self.finance.to_the_moon()
        self.assertTrue(self.finance._to_the_moon)
        self.assertEquals(ret, 'To the moooooooooon!')

    @_should_be_axon
    def test_return_to_earth(self):
        self.finance._to_the_moon = True
        self.assertTrue(self.finance._to_the_moon)
        ret = self.finance.return_to_earth()
        self.assertFalse(self.finance._to_the_moon)
        self.assertEquals(ret, 'Oh, fine :(')
