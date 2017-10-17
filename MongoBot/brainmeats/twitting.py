# -*- coding: utf-8 -*-
import logging

from MongoBot.autonomic import axon, help
from MongoBot.staff.publicist import Publicist
from MongoBot.synapses import Cerebellum, Receptor

logger = logging.getLogger(__name__)


@Cerebellum
class Twitting(object):
    def __init__(self):
        self.publicist = Publicist()

    @axon
    @help('<get link to twitter feed>')
    def twitter(self):
        return self.publicist.twitter_link()

    @axon
    @help('[ID] <retweet by id, or just the last seen tweet>')
    def retweet(self):
        try:
            self.publicist.retweet(self.stdin)
            return 'Retwitted'
        except Exception as e:
            return e.message

    def tweet(self):
        if not self.stdin:
            return 'Tweet what?'

        try:
            self.publicist.tweet(self.stdin)
            return 'Twitted'
        except Exception as e:
            return e.message

    @Receptor('overheard')
    def auto_get_tweet(self, incoming):
        message = incoming.stdin

        publicist = Publicist()
        tweet_id = publicist.get_tweet_id(message)

        if tweet_id:
            incoming.chat(publicist.get_tweet(tweet_id))
