# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import
import logging
import time
from MongoBot.synapses import Synapse
from MongoBot.utils import ratelimited
from slackclient import SlackClient

logger = logging.getLogger(__name__)


class Slack(object):

    def __init__(self, settings):

        self.provider = settings.__name__

        self.token = settings.token
        self.last_ping = 0

        self.client = SlackClient(self.token)

    def connect(self):

        logger.info('Connecting to Slack')
        self.client.rtm_connect()

    def ping(self):

        now = int(time.time())

        if now > self.last_ping + 3:
            self.client.server.ping()
            self.last_ping = now

    @ratelimited(2)
    def chat(self, message, target=None, error=False):

        self.client.rtm_send_message(target, message)

    def process(self):

        for reply in self.client.rtm_read():
            if 'type' in reply and reply['type'] == 'message':
                self.parse(reply)

        self.ping()

    @Synapse('MONGO_INCOMING_DATA')
    def parse(self, data):

        if 'text' not in data or 'user' not in data:
            return

        return {
            'provider': self.provider,
            'service': self.__class__.__name__,
            'module': self.__module__,
            'source': data['user'],
            'target': data['channel'],
            'data': data['text']
        }
