# -*- coding: utf-8 -*-
import mock

from MongoBot.brainmeats.reference import Reference
from tests.mocks.browser import MockBrowser
from tests.basket_case import BasketCase, should_be_axon


class TestReference(BasketCase):

    def setUp(self):
        self.setUpInstance(Reference)

    def test_Alien(self):
        self.assertIsInstance(self.instance, Reference)

    @mock.patch('MongoBot.brainmeats.reference.Browser', new=MockBrowser)
    @should_be_axon
    def test_is_it_down(self):
        self.instance.stdin = 'google.com'
        ret = self.instance.is_it_down()

        self.assertEquals(ret, '%s is up' % self.instance.stdin)

    @mock.patch('MongoBot.brainmeats.reference.Browser', new=MockBrowser)
    def test_is_it_down_yes_it_is(self):
        self.instance.stdin = 'moc.elgoog'
        ret = self.instance.is_it_down()

        self.assertEquals(ret, '%s is down' % self.instance.stdin)

    @mock.patch('MongoBot.brainmeats.reference.Browser', new=MockBrowser)
    def test_is_it_down_without_stdin(self):
        ret = self.instance.is_it_down()

        self.assertEquals(ret, 'Is what down?')

    @mock.patch('MongoBot.brainmeats.reference.Browser', side_effect=Exception)
    def test_is_it_down_exception(self, mocked_browser):
        self.instance.stdin = 'google.com'
        ret = self.instance.is_it_down()

        self.assertEquals(
            ret,
            ('downforeveryoneorjustme.com might be down for everyone...'
             'or just me?')
        )

    @should_be_axon
    def test_hack(self):
        ret = self.instance.hack()
        self.assertEquals(
            ret,
            ('Available functions: abs, acos, asin, atan, atan2, ceil, cos, '
             'cosh, degrees, e, exp, fabs, floor, fmod, frexp, hypot, ldexp, '
             'log, log10, modf, pi, pow, radians, sin, sinh, sqrt, tan, tanh')
        )

    def test_hack_69(self):
        self.instance.values = ['6 * 9']
        ret = self.instance.hack()

        self.assertEquals(ret, '42')

    def test_hack_kenfree_hax0r(self):
        self.instance.values = ['__']
        ret = self.instance.hack()

        self.assertEquals(ret, 'Rejected.')

    def test_hack_abs(self):
        self.instance.values = ['abs(-3)']
        ret = self.instance.hack()

        self.assertEquals(ret, '3')

    def test_hack_acos(self):
        self.instance.values = ['acos(-1)']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('3.1415926535'))

    def test_hack_asin(self):
        self.instance.values = ['asin(-1)']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('-1.5707963267'))

    def test_hack_atan(self):
        self.instance.values = ['atan(-1)']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('-0.78539816339'))

    def test_hack_atan2(self):
        self.instance.values = ['atan2(-1, 4)']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('-0.24497866312'))

    def test_hack_ceil(self):
        self.instance.values = ['ceil(1.23456)']
        ret = self.instance.hack()

        self.assertTrue(ret == '2' or ret == '2.0')

    def test_hack_cos(self):
        self.instance.values = ['cos(-1)']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('0.54030230586'))

    def test_hack_cosh(self):
        self.instance.values = ['cosh(-1)']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('1.5430806348'))

    def test_hack_degrees(self):
        self.instance.values = ['degrees(-1)']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('-57.295779513'))

    def test_hack_e(self):
        self.instance.values = ['1 + e']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('3.7182818284'))

    def test_hack_exp(self):
        self.instance.values = ['1 + exp(3)']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('21.085536923'))

    def test_hack_fabs(self):
        self.instance.values = ['1 + fabs(-3)']
        ret = self.instance.hack()

        self.assertEquals(ret, '4.0')

    def test_hack_floor(self):
        self.instance.values = ['1 + floor(7.123)']
        ret = self.instance.hack()

        self.assertTrue(ret == '8' or ret == '8.0')

    def test_hack_fmod(self):
        self.instance.values = ['1 + fmod(7.12, 8.41)']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('8.12'))

    def test_hack_frexp(self):
        self.instance.values = ['frexp(20)']
        ret = self.instance.hack()

        self.assertEquals(ret, '(0.625, 5)')

    def test_hack_hypot(self):
        self.instance.values = ['1 + hypot(12.12, 19.19)']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('23.696927104'))

    def test_hack_ldexp(self):
        self.instance.values = ['1 + ldexp(12, 19)']
        ret = self.instance.hack()

        self.assertEquals(ret, '6,291,457.0')

    def test_hack_log(self):
        self.instance.values = ['1 + log(12.12, 19.19)']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('1.8444577605'))

    def test_hack_log10(self):
        self.instance.values = ['1 + log10(12.12)']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('2.0835026198'))

    def test_hack_modf(self):
        self.instance.values = ['modf(20)']
        ret = self.instance.hack()

        self.assertEquals(ret, '(0.0, 20.0)')

    def test_hack_pi(self):
        self.instance.values = ['1 + pi']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('4.1415926535'))

    def test_hack_pow(self):
        self.instance.values = ['1 + pow(4, 5)']
        ret = self.instance.hack()

        self.assertTrue(ret == '1,025.0')

    def test_hack_radians(self):
        self.instance.values = ['1 + radians(4)']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('1.06981317'))

    def test_hack_sin(self):
        self.instance.values = ['1 + sin(4)']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('0.24319750'))

    def test_hack_sinh(self):
        self.instance.values = ['1 + sinh(4)']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('28.28991719'))

    def test_hack_sqrt(self):
        self.instance.values = ['1 + sqrt(45)']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('7.708203932'))

    def test_hack_tan(self):
        self.instance.values = ['1 + tan(45)']
        ret = self.instance.hack()

        self.assertTrue(ret.startswith('2.6197751905'))

    def test_hack_tanh(self):
        self.instance.values = ['1 + tanh(45)']
        ret = self.instance.hack()

        self.assertTrue(ret == '2' or ret == '2.0')

    def test_hack_type_error(self):
        self.instance.values = ['log10(1, 2)']
        ret = self.instance.hack()

        self.assertEquals(ret, 'log10() takes exactly one argument (2 given)')

    def test_hack_exception(self):
        self.instance.values = ['1 +/+ 1']
        self.instance.hack()

        self.assertActed('not smart enough to do that.')

    @mock.patch('MongoBot.staff.oracle.Browser', new=MockBrowser)
    @should_be_axon
    def test_ety(self):
        self.instance.values = ['test']
        ret = self.instance.ety()

        self.maxDiff = None
        self.assertEqual(
            ret,
            ('Etymology for ${bold:test (v.)} 1748, "to examine the '
             'correctness of," from test (n.), on the notion of "put to the '
             'proof." Earlier "assay gold or silver" in a test (c. 1600). '
             'Meaning "to administer a test" is from 1939; sense of "undergo a'
             ' test" is from 1934. Related: ${bold:Tested}; ${bold:testing}. ')
        )

    @mock.patch('MongoBot.staff.oracle.Browser', new=MockBrowser)
    def test_ety_no_results(self):
        self.instance.values = ['adsfgkhadljsg']
        ret = self.instance.ety()

        self.assertEqual(
            ret,
            ('Could not find the etymology for adsfgkhadljsg')
        )

    def test_ety_no_search_word(self):
        self.instance.values = []
        ret = self.instance.ety()

        self.assertEqual(ret, 'Find the etymology of what?')
