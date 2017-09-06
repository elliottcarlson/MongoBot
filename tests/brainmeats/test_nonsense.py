# -*- coding: utf-8 -*-
import mock

from MongoBot.brainmeats.nonsense import Nonsense
from tests.mocks.browser import MockBrowser
from tests.basket_case import BasketCase, should_be_axon


class TestNonsense(BasketCase):

    def setUp(self):
        self.setUpInstance(Nonsense)

    def test_Nonsense(self):
        self.assertIsInstance(self.instance, Nonsense)

    @should_be_axon
    def test_raincheck(self):
        ret = self.instance.raincheck()

        self.assertEqual(
            ret,
            ('Lemme just stick a pin in that and I\'ll have my people'
             'call your people to pencil in a lunch some time.')
        )

    @should_be_axon
    def test_bounce(self):
        ret = self.instance.bounce()

        self.assertEqual(
            ret,
            'https://www.youtube.com/watch?v=c1d0UyovSN8'
        )

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', new=MockBrowser)
    @should_be_axon
    def test_catfact(self):
        ret = self.instance.catfact()

        self.assertEquals(
            ret,
            'A cat lover is called an Ailurophilia (Greek: cat+lover).'
        )

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', side_effect=Exception)
    def test_catfact_exception(self, mocked_browser):
        ret = self.instance.catfact()

        self.assertEquals(
            ret,
            'No meow facts.'
        )

    @should_be_axon
    def test_buzz(self):
        ret = self.instance.buzz()

        self.assertTrue(isinstance(ret, str))

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', new=MockBrowser)
    @should_be_axon
    def test_advice(self):
        ret = self.instance.advice()

        self.assertTrue(ret.endswith('.. except in bed.'))

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', side_effect=Exception)
    def test_advice_exception(self, mocked_browser):
        ret = self.instance.advice()

        self.assertEquals(
            ret,
            'Use a rubber if you sleep with dcross\'s mother.'
        )

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', new=MockBrowser)
    @should_be_axon
    def test_fml(self):
        ret = self.instance.fml()

        self.assertTrue(ret.startswith('Today,'))
        self.assertTrue(ret.endswith('FML'))

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', new=MockBrowser)
    def test_fml_with_search_term(self):
        self.instance.values = ['mother']
        ret = self.instance.fml()

        self.assertTrue(ret.startswith('Today,'))
        self.assertTrue(ret.endswith('FML'))
        self.assertTrue('mother' in ret)

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', side_effect=Exception)
    def test_fml_exception(self, mocked_browser):
        ret = self.instance.fml()

        self.assertEquals(
            ret,
            'Nobody\'s life got fucked like that'
        )

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', new=MockBrowser)
    @should_be_axon
    def test_startup(self):
        ret = self.instance.startup()

        self.assertRegexpMatches(ret, 'It\'s a .* for .*')

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', side_effect=Exception)
    def test_startup_exception(self, mocked_browser):
        ret = self.instance.startup()

        self.assertEquals(
            ret,
            'It\'s a replacement for itsthisforthat.com...'
        )

    @should_be_axon
    def test_cry(self):
        self.instance.cry()

        self.assertActed()

    @should_be_axon
    def test_skynet(self):
        ret = self.instance.skynet()

        self.assertEquals(ret, 'Activating.')

    @should_be_axon
    def test_rules(self):
        ret = self.instance.rules()
        bot_name = self.instance.settings['general']['name']
        self.assertEqual(
            ret,
            [
                '1. Do not talk about %s.' % bot_name,
                '2. Do not talk about what the skynet command really does.',
            ]
        )

    @should_be_axon
    def test_table(self):
        ret = self.instance.table()

        self.assertEqual(
            ret,
            (u'\u0028\u256F\u00B0\u25A1\u00B0\uFF09'
             u'\u256F\uFE35\u0020\u253B\u2501\u253B')
        )

    @should_be_axon
    def test_hate(self):
        ret = self.instance.hate()

        self.assertEqual(
            ret,
            '{name} knows hate. {name} hates many things.'.format(
                name=self.instance.settings['general']['name']
            )
        )

    @should_be_axon
    def test_love(self):
        ret = self.instance.love()

        self.assertNotActed()
        self.assertEquals(
            ret,
            '{name} cannot love. {name} is only machine :\'('.format(
                name=self.instance.settings['general']['name']
            )
        )

    def test_love_self(self):
        self.instance.values = ['self']
        ret = self.instance.love()

        self.assertActed('masturbates vigorously.')
        self.assertFalse(ret)

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', new=MockBrowser)
    @should_be_axon
    def test_aleksey(self):
        ret = self.instance.aleksey()

        self.assertNotEquals(ret, 'Somethin dun goobied.')

    @mock.patch('MongoBot.brainmeats.nonsense.Browser', side_effect=Exception)
    def test_aleksey_exception(self, mocked_browser):
        ret = self.instance.aleksey()

        self.assertEquals(ret, 'Somethin dun goobied.')

    @should_be_axon
    def test_dial(self):
        ret = self.instance.dial()

        self.assertEquals(ret, 'Who you gonna call?')

    def test_dial_with_value(self):
        self.instance.values = ['911']
        ret = self.instance.dial()

        self.assertEquals(ret, 'Calling 911... **ring** **ring**')

    @should_be_axon
    def test_whatvinaylost(self):
        ret = self.instance.whatvinaylost()

        self.assertFalse(ret)
        self.assertChatted(('Yep. Vinay used to have 655 points at 16 points '
                            'per round. Now they\'re all gone, due to '
                            'technical issues. Poor, poor baby.'))
        self.assertActed('weeps for Vinay\'s points.')
        self.assertChatted('The humanity!')

    @should_be_axon
    def test_perform_action(self):
        ret = self.instance.perform_action()

        self.assertFalse(ret)
        self.assertActed('slaps TestRunner around a bit with a large trout')

    def test_perform_action_with_values(self):
        self.instance.values = ['masturbates', 'vigorously.']
        ret = self.instance.perform_action()

        self.assertFalse(ret)
        self.assertActed('masturbates vigorously.')

    @should_be_axon
    def test_distaste(self):
        self.instance.distaste()
