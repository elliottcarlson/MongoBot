# -*- coding: utf-8 -*-
import logging

from importlib import import_module
from MongoBot.cortex import Cortex
from MongoBot.hyperthymesia import load_config
from MongoBot.staff.butler import Butler
from MongoBot.synapses import Cerebellum, Receptor

logger = logging.getLogger(__name__)


@Cerebellum
class Thalamus(object):
    """
    The thalamus is the large mass of gray matter in the dorsal part of the
    diencephalon of the brain with several functions such as relaying of
    sensory and motor signals to the cerebral cortex, and the regulation of
    consciousness, sleep, and alertness.

    Mongo's thalamus handles the regulation of connectivity to it's bodym such
    as Slack or IRC.
    """
    providers = {}

    def __init__(self):
        """
        Determine which services we will be connecting to from the config file.
        """
        self.settings = load_config('./config/settings.yaml')

        for key in self.settings.services:
            service = self.settings.services[key]

            if service.enabled:
                (module, class_name) = service.module.rsplit('.', 1)
                settings = service.settings
                settings.__name__ = key
                provider = getattr(import_module(module), class_name)(settings)
                self.providers[key] = provider

    def connect(self):
        """
        Connect to all known service providers.
        """
        for provider in self.providers:
            self.providers[provider].connect()

    def process(self):
        """
        Process incoming data from the services.
        """
        for provider in self.providers:
            self.providers[provider].process()

    @Receptor('MONGO_INCOMING_DATA')
    def parse_incoming(self, data):
        """
        Parse incoming data via the Cortex - Butler this off for threading.
        """
        butler = Butler()
        butler.do(Cortex.comprehend, data)
