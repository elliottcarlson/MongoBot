# -*- coding: utf-8 -*-
import logging
import random

from MongoBot.autonomic import axon, help
from praw import Reddit

logger = logging.getLogger(__name__)


class Alien(object):

    @axon('r(eddit)?')
    @help('<grab reddit stuff>')
    def reddit(self):
        try:
            config = {
                'user_agent': self.config.get('user_agent'),
                'client_id': self.config.get('client_id'),
                'client_secret': self.config.get('client_secret')
            }

            if None in config.viewvalues():
                raise Exception('One of Aliens config values is not set!')
        except Exception as e:
            """
            We need an alien.yaml in the config directory that contains the
            user_agent, client_id, and client_secret.
            """
            logger.exception(e)
            return 'Reddit not configured properly :('

        api = Reddit(**config)
        subreddit = False

        if not self.values:
            subreddit = 'random'
        else:
            subreddit = self.values[0]

        try:
            posts = api.subreddit(subreddit).hot(limit=5)

            entries = []
            for post in posts:
                entries.append(
                    '[/r/%s] %s %s' % (
                        post.subreddit.display_name,
                        post.title,
                        post.shortlink
                    )
                )

            entry = random.choice(entries)
        except Exception as e:
            return 'Reddit fail. %s' % str(e)

        return entry
