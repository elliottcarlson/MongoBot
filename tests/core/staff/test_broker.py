# -*- coding: utf-8 -*-
import logging
import mock
import unittest

from MongoBot.staff.broker import Broker
from tests.mocks.browser import MockBrowser

logger = logging.getLogger(__name__)


class TestBroker(unittest.TestCase):

    @mock.patch('MongoBot.staff.broker.Browser', new=MockBrowser)
    def test_broker_setup(self):
        broker = Broker('AGNC')
        self.assertIsInstance(broker, Broker)

    def test_broker_no_symbol(self):
        broker = Broker(None)
        quote = broker.showquote()

        self.assertFalse(broker)
        self.assertFalse(quote)

        self.assertFalse(broker.__nonzero__())
        self.assertFalse(broker.__bool__())

    @mock.patch('MongoBot.staff.broker.Browser', new=MockBrowser)
    def test_broker_showquote_down(self):
        broker = Broker('AGNC')
        quote = broker.showquote()

        self.assertEquals(
            quote,
            ('AGNC Investment Corp. (AGNC), 21.3, '
             '${red:-0.15 (0.70%)}, http://roa.st/000')
        )

    @mock.patch('MongoBot.staff.broker.Browser', new=MockBrowser)
    def test_broker_showquote_up(self):
        broker = Broker('BF-B')
        quote = broker.showquote()

        self.assertEquals(
            quote,
            ('Brown Forman Inc Class B (BF-B), 53.46, ${green:0.08 (0.15%)}, '
             'http://roa.st/000')
        )

    @mock.patch('MongoBot.staff.broker.Browser', new=MockBrowser)
    def test_broker_dot_to_dash(self):
        broker = Broker('BF.B')
        self.assertEquals(broker.symbol, 'BF-B')

    @mock.patch('logging.Logger.exception')
    @mock.patch('MongoBot.staff.broker.Browser', new=Exception)
    def test_broker_browser_exception(self, mock_logger):
        Broker('TEST')
        mock_logger.assert_called()

    @mock.patch('MongoBot.staff.broker.Browser', new=MockBrowser)
    def test_broker_missing_exchange(self):
        ret = Broker('TWTR')

        self.assertFalse(ret)
