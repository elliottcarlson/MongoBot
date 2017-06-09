# -*- coding: utf-8 -*-

from MongoBot.synapses import Cerebellum, Receptor
from MongoBot.thalami.IRC import IRC
from MongoBot.thalami.Slack import Slack

"""
The thalamus is the large mass of gray matter in the dorsal part of the
diencephalon of the brain with several functions such as relaying of sensory
and motor signals to the cerebral cortex, and the regulation of consciousness,
sleep, and alertness.

In MongoBot, the Thalamus handles the regulation of connectivity to it's body,
such as IRC or Slack.
"""
@Cerebellum
class Thalamus(object):

    def __init__(self):

        self.irc = IRC()
        self.slack = Slack('xoxb-195965876935-PslSW24yOGtASNo9YqHy5SkZ')

    def connect(self):

        #self.irc.connect()
        self.slack.connect()

    def process(self):

        #self.irc.process()
        self.slack.process()

    @Receptor('THALAMUS_DATA')
    def test(self, *args):
        from pprint import pprint
        print('In thalamus receptor...')
        pprint(args)
