# -*- coding: utf-8 -*-

from importlib import import_module
from MongoBot.hyperthymesia import load_config
from MongoBot.synapses import Cerebellum, Receptor
import sys


@Cerebellum
class Thalamus(object):
    """
    The thalamus is the large mass of gray matter in the dorsal part of the
    diencephalon of the brain with several functions such as relaying of
    sensory and motor signals to the cerebral cortex, and the regulation of
    consciousness, sleep, and alertness.

    In MongoBot, the Thalamus handles the regulation of connectivity to it's
    body, such as IRC or Slack.
    """

    def __init__(self):

        self.providers = dict()
        self.settings = load_config('./config/settings.yaml')

        for service in self.settings.services.values():
            if service.enabled:
                module, class_name = service.module.rsplit('.', 1)
                settings = service.settings
                provider = getattr(import_module(module), class_name)(settings)
                self.providers[class_name] = provider

    def connect(self):

        for provider in self.providers:
            self.providers[provider].connect()

    def process(self):

        for provider in self.providers:
            self.providers[provider].process()

    @Receptor('THALAMUS_DATA')
    def test(self, *args):
        from pprint import pprint
        print('In thalamus receptor...')
        pprint(args)
