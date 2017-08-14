import mock
import sys
import unittest

from MongoBot.brainmeats.finance import Finance
from tests.mocks.broker import MockBroker


class TestFinance(unittest.TestCase):

    def setUp(self):
        # MongoBot.brainmeats.finance.Broker
        self.finance = Finance()

    def test_Finance(self):
        self.assertIsInstance(self.finance, Finance)

    def test_q_has_axon(self):
        self.assertTrue(hasattr(self.finance.q, 'axon'))

    def test_q_has_help(self):
        self.assertTrue(hasattr(self.finance.q, 'help'))
        self.assertEquals(self.finance.q.help, 'STOCK_SYMBOL <get stock quote>')

    @mock.patch('MongoBot.brainmeats.finance.Broker')
    def test_q_valid_quote(self, mocked):
        self.finance.stdin = 'GOOG'
        mocked.return_value = MockBroker(self.finance.stdin)
        ret = self.finance.q()
        self.assertEquals(
            ret,
            'Alphabet Inc. (GOOG), 914.39, ${green:7.15 (0.79%)}, http://roa.st/cok'
        )

    @mock.patch('MongoBot.brainmeats.finance.Broker')
    def test_q_invalid_quote(self, mocked):
        self.finance.stdin = 'INVALID'
        mocked.return_value = MockBroker(self.finance.stdin)
        ret = self.finance.q()
        self.assertEquals(ret, 'Couldn\'t find company: INVALID')

    @mock.patch('MongoBot.brainmeats.finance.Broker')
    def test_q_no_quote(self, mocked):
        self.finance.stdin = None
        mocked.return_value = MockBroker(self.finance.stdin)
        ret = self.finance.q()
        self.assertEquals(ret, 'Couldn\'t find company: None')
