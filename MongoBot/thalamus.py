# -*- coding: utf-8 -*-

from importlib import import_module
from MongoBot.hyperthymesia import load_config
from MongoBot.cortex import Cortex
from MongoBot.synapses import Cerebellum, Receptor


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
    providers = {}

    def __init__(self):

        # self.providers = dict()
        self.settings = load_config('./config/settings.yaml')

        print(self.settings)

        for key, service in self.settings.services.items():
            if service.enabled:
                module, class_name = service.module.rsplit('.', 1)
                settings = service.settings
                settings.__name__ = key
                provider = getattr(import_module(module), class_name)(settings)
                self.providers[key] = provider

    def connect(self):

        for provider in self.providers:
            self.providers[provider].connect()

    def process(self):

        for provider in self.providers:
            Thalamus.providers[provider].process()

    @Receptor('THALAMUS_INCOMING_DATA')
    def parse_incoming(self, data):

        Cortex.interpret(data)
