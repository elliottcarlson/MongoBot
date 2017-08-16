import mock
import os
import unittest

from MongoBot.brainmeats.nonsense import Nonsense
from MongoBot.hyperthymesia import load_config
from tests.mocks.browser import MockBrowser

class TestNonsense(unittest.TestCase):
    mocks = {}

    def setUp(self):
        self.nonsense = Nonsense()
        self.nonsense.values = []

        self.nonsense.source = 'TestRunner'

        self.mocks['chat'] = False
        self.mock_chats = []
        self.nonsense.chat = self._mock_chat

        self.mocks['act'] = False
        self.mock_actions = []
        self.nonsense.act = self._mock_act

        config_file = './config/nonsense.yaml'
        if os.path.isfile(config_file):
            self.nonsense.config = load_config(config_file)

        self.nonsense.settings = load_config('./config/settings.yaml')

    def _mock_act(self, action):
        """
        Register when self.act() is called from a brainmeats.
        """
        self.mocks['act'] = True
        self.mock_actions.append(action)

    def assertActed(self, action=None):
        if action:
            return (action in self.mock_actions)
        else:
            return self.mocks['act']

    def _mock_chat(self, message):
        """
        Register when self.chat() is called from a brainmeats.
        """
        self.mocks['chat'] = True
        self.mock_chats.append(message)

    def assertChatted(self, message=None):
        if message:
            return (message in self.mock_chats)
        else:
            return self.mocks['chat']

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
            func_root = getattr(self.nonsense, func_name)
            self.assertTrue(hasattr(func_root, 'axon'))
            func(self)

        return check

    def test_Nonsense(self):
        self.assertIsInstance(self.nonsense, Nonsense)

    @_should_be_axon
    def test_raincheck(self):
        ret = self.nonsense.raincheck()

        self.assertEqual(
            ret,
            ('Lemme just stick a pin in that and I\'ll have my people'
             'call your people to pencil in a lunch some time.')
        )

    @_should_be_axon
    def test_bounce(self):
        ret = self.nonsense.bounce()

        self.assertEqual(
            ret,
            'https://www.youtube.com/watch?v=c1d0UyovSN8'
        )

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', new=MockBrowser)
    @_should_be_axon
    def test_catfact(self):
        ret = self.nonsense.catfact()

        self.assertEquals(
            ret,
            ('The average lifespan of an outdoor-only cat is about 3 to 5 '
             'years while an indoor-only cat can live 16 years or much longer.')
        )

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', side_effect=Exception)
    def test_catfact_exception(self, mocked_browser):
        ret = self.nonsense.catfact()

        self.assertEquals(
            ret,
            'No meow facts.'
        )

    @_should_be_axon
    def test_buzz(self):
        ret = self.nonsense.buzz()

        self.assertTrue(isinstance(ret, str))

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', new=MockBrowser)
    @_should_be_axon
    def test_advice(self):
        ret = self.nonsense.advice()

        self.assertTrue(ret.endswith('.. except in bed.'))

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', side_effect=Exception)
    def test_advice_exception(self, mocked_browser):
        ret = self.nonsense.advice()

        self.assertEquals(
            ret,
            'Use a rubber if you sleep with dcross\'s mother.'
        )

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', new=MockBrowser)
    @_should_be_axon
    def test_fml(self):
        ret = self.nonsense.fml()

        self.assertTrue(ret.startswith('Today,'))
        self.assertTrue(ret.endswith('FML'))

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', new=MockBrowser)
    def test_fml_with_search_term(self):
        self.nonsense.values = ['mother']
        ret = self.nonsense.fml()

        self.assertTrue(ret.startswith('Today,'))
        self.assertTrue(ret.endswith('FML'))
        self.assertTrue('mother' in ret)

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', side_effect=Exception)
    def test_fml_exception(self, mocked_browser):
        ret = self.nonsense.fml()

        self.assertEquals(
            ret,
            'Nobody\'s life got fucked like that'
        )

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', new=MockBrowser)
    @_should_be_axon
    def test_startup(self):
        ret = self.nonsense.startup()

        self.assertRegexpMatches(ret, 'It\'s a .* for .*')

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', side_effect=Exception)
    def test_startup_exception(self, mocked_browser):
        ret = self.nonsense.startup()

        self.assertEquals(
            ret,
            'It\'s a replacement for itsthisforthat.com...'
        )

    @_should_be_axon
    def test_cry(self):
        self.nonsense.cry()

        self.assertTrue(self.mocks['act'])

    @_should_be_axon
    def test_skynet(self):
        ret = self.nonsense.skynet()

        self.assertEquals(ret, 'Activating.')

    @_should_be_axon
    def test_rules(self):
        ret = self.nonsense.rules()

        self.assertEqual(
            ret,
            [
                '1. Do not talk about %s.' % self.nonsense.settings['general']['name'],
                '2. Do not talk about what the skynet command really does.',
            ]
        )

    @_should_be_axon
    def test_table(self):
        ret = self.nonsense.table()

        self.assertEqual(
            ret,
            u'\u0028\u256F\u00B0\u25A1\u00B0\uFF09\u256F\uFE35\u0020\u253B\u2501\u253B'
        )

    @_should_be_axon
    def test_hate(self):
        ret = self.nonsense.hate()

        self.assertEqual(
            ret,
            '{name} knows hate. {name} hates many things.'.format(
                name=self.nonsense.settings['general']['name']
            )
        )

    @_should_be_axon
    def test_love(self):
        ret = self.nonsense.love()

        self.assertFalse(self.mocks['act'])
        self.assertEquals(
            ret,
            '{name} cannot love. {name} is only machine :\'('.format(
                name=self.nonsense.settings['general']['name']
            )
        )

    def test_love_self(self):
        self.nonsense.values = ['self']
        ret = self.nonsense.love()

        self.assertTrue(self.mocks['act'])
        self.assertTrue('masturbates vigorously.' in self.mock_actions)
        self.assertFalse(ret)

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', new=MockBrowser)
    @_should_be_axon
    def test_aleksey(self):
        ret = self.nonsense.aleksey()

        self.assertNotEquals(ret, 'Somethin dun goobied.')

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', side_effect=Exception)
    def test_aleksey_exception(self, mocked_browser):
        ret = self.nonsense.aleksey()

        self.assertEquals(ret, 'Somethin dun goobied.')

    @_should_be_axon
    def test_dial(self):
        ret = self.nonsense.dial()

        self.assertEquals(ret, 'Who you gonna call?')

    def test_dial_with_value(self):
        self.nonsense.values = ['911']
        ret = self.nonsense.dial()

        self.assertEquals(ret, 'Calling 911... **ring** **ring**')

    @_should_be_axon
    def test_whatvinaylost(self):
        ret = self.nonsense.whatvinaylost()

        self.assertFalse(ret)
        self.assertChatted(('Yep. Vinay used to have 655 points at 16 points '
                            'per round. Now they\'re all gone, due to '
                            'technical issues. Poor, poor baby.'))
        self.assertActed('weeps for Vinay\'s points.')
        self.assertChatted('The humanity!')

    @_should_be_axon
    def test_perform_action(self):
        ret = self.nonsense.perform_action()

        self.assertFalse(ret)
        self.assertChatted('slaps TestRunner around a bit with a large trout')

    def test_perform_action_with_values(self):
        self.values = ['masturbates', 'vigorously.']
        ret = self.nonsense.perform_action()

        self.assertFalse(ret)
        self.assertChatted('maturbates vigorously.')

    @_should_be_axon
    def test_distaste(self):
        ret = self.nonsense.distaste()
