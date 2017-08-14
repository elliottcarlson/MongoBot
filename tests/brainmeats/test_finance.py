import mock
import sys
import unittest

from MongoBot.brainmeats.finance import Finance


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
        ret = self.finance.q()
        self.assertTrue(ret.startswith('Alphabet Inc. (GOOG)'))

    def test_q_invalid_quote(self):
        self.finance.stdin = 'INVALID'
        ret = self.finance.q()
        self.assertEquals(ret, 'Couldn\'t find company: INVALID')
