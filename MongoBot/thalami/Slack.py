# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import
import json
import logging
import time

from pprint import pprint
from slackclient import SlackClient


logger = logging.getLogger(__name__)


class Slack(object):

    def __init__(self, settings):

        self.token = settings.token
        self.last_ping = 0

        self.client = SlackClient(self.token)

    def connect(self):

        self.client.rtm_connect()


    def ping(self):

        now = int(time.time())

        if now > self.last_ping + 3:
            self.client.server.ping()
            self.last_ping = now


    def process(self):

        for reply in self.client.rtm_read():

            pprint(reply)

        self.ping()

