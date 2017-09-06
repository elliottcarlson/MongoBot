import unittest

from MongoBot.wernicke import Wernicke
from pyparsing import Dict


class TestWernicke(unittest.TestCase):
    """Test for MongoBot/wernicke.py"""

    def setUp(self):
        self.parser = Wernicke(command_prefix='*', multi_prefix='^')

    def test_Wernicke(self):

        self.assertIsInstance(self.parser, Wernicke)

    def test_EBNF_Dict(self):

        self.assertIsInstance(self.parser.EBNF, Dict)

    def test_no_command(self):

        ret = self.parser.parse('this is a test without a command')
        self.assertEquals(ret, None)

    def test_single_command(self):

        ret = self.parser.parse('*hack 0.475 + 0.749')
        self.assertIsInstance(ret, list)
        self.assertEquals(ret, [[['*', 'hack'], ['0.475', '+', '0.749']]])

    def test_multi_command(self):

        ret = self.parser.parse('^c eth etc btc bcc')
        self.assertIsInstance(ret, list)
        self.assertEquals(ret, [[['^', 'c'], ['eth', 'etc', 'btc', 'bcc']]])

    def test_forked_command(self):

        ret = self.parser.parse('*fml junk | *sms 555-1010')
        self.assertIsInstance(ret, list)
        self.assertEquals(
            ret,
            [[['*', 'fml'], ['junk']], [['*', 'sms'], ['555-1010']]]
        )

    def test_multiple_forked_commands(self):

        ret = self.parser.parse('*one | *two | *three | *four')
        self.assertIsInstance(ret, list)
        self.assertEquals(
            ret,
            [[['*', 'one']], [['*', 'two']], [['*', 'three']], [['*', 'four']]]
        )

    def test_forked_to_no_command(self):

        ret = self.parser.parse('*fml junk | not a command')
        self.assertIsInstance(ret, list)
        self.assertEquals(ret, [[['*', 'fml'], ['junk']]])

    def test_malformed_command(self):

        ret = self.parser.parse('**test')
        self.assertEquals(ret, None)

    def test_malformed_multi_command(self):

        ret = self.parser.parse('^^test')
        self.assertEquals(ret, None)
