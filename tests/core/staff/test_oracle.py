# -*- coding: utf-8 -*-
import logging
import mock
import unittest

from MongoBot.staff.oracle import Oracle
from tests.mocks.browser import MockBrowser

logger = logging.getLogger(__name__)


class TestOracle(unittest.TestCase):

    @mock.patch('MongoBot.staff.broker.Browser', new=MockBrowser)
    def test_oracle_setup(self):
        oracle = Oracle('word')

        self.assertIsInstance(oracle, Oracle)
        self.assertEquals(oracle.search, 'word')

    @mock.patch('MongoBot.staff.oracle.Browser', new=MockBrowser)
    def test_oracle_query_etymonline(self):
        oracle = Oracle()
        res = oracle.query_etymonline('test')

        self.assertEquals(res[0][0], 'test (v.)')

    def test_oracle_random_word(self):
        oracle = Oracle()
        res = oracle.get_random_word()

        self.assertIsInstance(res, str)
