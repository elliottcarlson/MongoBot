# -*- coding: utf-8 -*-
import mock

from MongoBot.brainmeats.alien import Alien
from tests.mocks.praw import MockPraw
from tests.basket_case import BasketCase, should_be_axon


class TestAlien(BasketCase):

    def setUp(self):
        self.setUpInstance(Alien)

    def test_Alien(self):
        self.assertIsInstance(self.instance, Alien)

    @mock.patch('MongoBot.brainmeats.alien.Reddit', new=MockPraw)
    @should_be_axon
    def test_reddit(self):
        self.instance.values = ['mildlyinteresting']
        ret = self.instance.reddit()

        self.assertTrue(ret.startswith('[/r/%s]' % self.instance.values[0]))

    @mock.patch('MongoBot.brainmeats.alien.Reddit', new=MockPraw)
    def test_reddit_without_value(self):
        ret = self.instance.reddit()

        self.assertTrue(ret.startswith('[/r/random]'))

    @mock.patch('MongoBot.brainmeats.alien.Reddit', new=MockPraw)
    def test_reddit_without_config_file(self):
        del(self.instance.config)
        ret = self.instance.reddit()

        self.assertEquals(ret, 'Reddit not configured properly :(')

    @mock.patch('MongoBot.brainmeats.alien.Reddit', new=MockPraw)
    def test_reddit_with_missing_config_value(self):
        self.instance.config['client_id'] = None
        ret = self.instance.reddit()

        self.assertEquals(ret, 'Reddit not configured properly :(')

    @mock.patch('MongoBot.brainmeats.alien.Reddit', new=MockPraw)
    def test_reddit_subreddit_exception(self):
        self.instance.values = ['spacedicks']
        ret = self.instance.reddit()

        self.assertEquals(ret, 'Reddit fail. No one should see /r/spacedicks')
