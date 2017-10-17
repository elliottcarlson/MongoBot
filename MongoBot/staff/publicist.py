# -*- coding: utf-8 -*-
import logging
import re
import sys
import tweepy

from MongoBot.hyperthymesia import load_config

logger = logging.getLogger(__name__)


class Publicist(object):
    """
    The Publicist handles all of MongoBot's publicity stunts, and most
    importantly his social media precense. You didn't expect him to do that all
    on his own did you?
    """
    last_tweet = None

    def __init__(self):
        self.config = load_config('config/staff.yaml').get('publicist')

        auth = tweepy.OAuthHandler(
            self.config.get('twitter_consumer_key'),
            self.config.get('twitter_consumer_secret')
        )
        auth.set_access_token(
            self.config.get('twitter_access_token'),
            self.config.get('twitter_access_secret')
        )
        self.twitter = tweepy.API(auth)

    def twitter_link(self):
        return self.config.get('twitter_link')

    def retweet(self, source=None):
        tweet_id = source

        if not source and not Publicist.last_tweet:
            raise AttributeError('Source not provided and no prior tweet id.')

        if source:
            tweet_id = self.get_tweet_id(source)

        if not tweet_id:
            tweet_id = Publicist.last_tweet

        try:
            self.twitter.retweet(tweet_id)
            return True
        except Exception as e:
            logger.exception(e)
            exc_info = sys.exc_info()
            raise exc_info[0], exc_info[1], exc_info[2]

    def tweet(self, message):
        if type(message) not in (str, unicode):
            raise TypeError('Untweetable.')

        try:
            self.twitter.update_status(message)
            return True
        except Exception as e:
            logger.exception(e)
            exc_info = sys.exc_info()
            raise exc_info[0], exc_info[1], exc_info[2]

    def get_tweet(self, source):
        tweet_id = self.get_tweet_id(source)

        if not tweet_id:
            raise TypeError('Not a valid tweet source.')

        Publicist.last_tweet = tweet_id

        status = self.twitter.get_status(tweet_id)
        text = status.text
        screen_name = status.user.screen_name
        name = status.user.name

        return {
            'text': text,
            'screen_name': screen_name,
            'name': name
        }

    def get_tweet_id(self, source):
        if source and source.isdigit():
            return source

        pattern = r'http[s]?://[www\.]?twitter\.com/.+/status/([0-9]+)'
        source = re.findall(pattern, source)

        if len(source):
            return source.pop()

        return False
