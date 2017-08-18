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
