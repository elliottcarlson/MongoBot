# -*- coding: utf-8 -*-
import logging

from importlib import import_module
from MongoBot.cortex import Cortex
from MongoBot.dendrite import Dendrite
from MongoBot.hyperthymesia import load_config
from MongoBot.staff.butler import Butler
from MongoBot.synapses import Cerebellum, Receptor, Synapse

logger = logging.getLogger(__name__)


@Cerebellum
class Thalamus(object):
    """
    The thalamus is the large mass of gray matter in the dorsal part of the
    diencephalon of the brain with several functions such as relaying of
    sensory and motor signals to the cerebral cortex, and the regulation of
    consciousness, sleep, and alertness.

    Mongo's thalamus handles the regulation of connectivity to it's body, such
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

    @Synapse('heartbeat')
    def process(self):
        """
        Process incoming data from the services. This method is constantly
        running and processing everything that happens. This means it is also
        the perfect place to send out a synapse of the heart beat for anything
        else that wishes to remain in cyclic sync with the core system.
        """
        for provider in self.providers:
            self.providers[provider].process()

    @Receptor('__data')
    @Synapse('overheard')
    def parse_incoming(self, data):
        """
        Parse incoming data via the Cortex - Butler this off for threading,
        also send out an `overheard` Synapse for all the Receptors that care.
        """
        butler = Butler()
        butler.do(Cortex.comprehend, data)

        data['stdin'] = data['data']
        data = Dendrite(data, [], Cortex.thalamus)
        return data
