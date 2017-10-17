# -*- coding: utf-8 -*-
import mock
import unittest

from MongoBot.staff.publicist import Publicist
from tests.mocks.mock_requests import MockRequest


class TestPublicist(unittest.TestCase):

    @mock.patch('tweepy.API', return_value=mock.MagicMock)
    def test_publicist_setup(self, mock_):
        publicist = Publicist()
        self.assertIsInstance(publicist, Publicist)

    def test_publicist_twitter_link(self):
        publicist = Publicist()
        publicist.config['twitter_link'] = 'test twitter link'
        self.assertEquals(publicist.twitter_link(), 'test twitter link')

    @mock.patch('requests.Session', side_effect=MockRequest.Session)
    def test_publicist_get_tweet_with_id(self, mock_session):
        publicist = Publicist()
        ret = publicist.get_tweet('905092446715092992')

        self.assertIn('name', ret)
        self.assertIn('screen_name', ret)
        self.assertIn('text', ret)
        self.assertEquals(ret.get('name'), 'Mongo Bot')
        self.assertEquals(ret.get('screen_name'), 'BotMongo')
        self.assertEquals(
            ret.get('text'), 'aromatic jam, such honey-and-nut sweets'
        )

    @mock.patch('requests.Session', side_effect=MockRequest.Session)
    def test_publicist_get_tweet_with_url(self, mock_session):
        publicist = Publicist()
        ret = publicist.get_tweet(
            'https://twitter.com/BotMongo/status/905092446715092992'
        )

        self.assertIn('name', ret)
        self.assertIn('screen_name', ret)
        self.assertIn('text', ret)
        self.assertEquals(ret.get('name'), 'Mongo Bot')
        self.assertEquals(ret.get('screen_name'), 'BotMongo')
        self.assertEquals(
            ret.get('text'), 'aromatic jam, such honey-and-nut sweets'
        )

    @mock.patch('requests.Session', side_effect=MockRequest.Session)
    def test_publicist_get_tweet_invalid_source(self, mock_session):
        publicist = Publicist()
        with self.assertRaises(TypeError):
            publicist.get_tweet('abcdefgh')

    @mock.patch('requests.Session', side_effect=MockRequest.Session)
    def test_publicist_update_status(self, mock_session):
        publicist = Publicist()
        self.assertTrue(publicist.tweet(
            'Who monitors New Relic when New Relic is down?'
        ))

    @mock.patch('requests.Session', side_effect=MockRequest.Session)
    def test_publicist_update_status_typeerror_exception(self, mock_session):
        publicist = Publicist()
        with self.assertRaises(TypeError):
            publicist.tweet({})

    @mock.patch('tweepy.API.update_status', side_effect=Exception)
    def test_publicist_update_status_tweet_exception(self, mock_tweepy):
        publicist = Publicist()
        with self.assertRaises(Exception):
            publicist.tweet('Y U TWEET DIS?!')

    @mock.patch('tweepy.API.retweet', side_effect=Exception)
    def test_publicist_retweet_without_source_or_last_tweet(self, mock_tweepy):
        publicist = Publicist()
        Publicist.last_tweet = None
        with self.assertRaises(AttributeError):
            publicist.retweet()

    @mock.patch('requests.Session', side_effect=MockRequest.Session)
    def test_publicist_retweet_with_source(self, mock_session):
        publicist = Publicist()
        self.assertTrue(publicist.retweet('917508391622164480'))

    @mock.patch('tweepy.API.retweet')
    def test_publicist_retweet_with_last_tweet(self, mock_tweepy):
        publicist = Publicist()
        Publicist.last_tweet = '1234567890'
        publicist.retweet()
        mock_tweepy.assert_called_with('1234567890')

    @mock.patch('tweepy.API.retweet', side_effect=Exception)
    def test_publicist_retweet_exception(self, mock_tweepy):
        publicist = Publicist()
        with self.assertRaises(Exception):
            publicist.retweet('905092446715092992')
