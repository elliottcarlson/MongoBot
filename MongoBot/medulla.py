# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
from MongoBot.cortex import Cortex
from MongoBot.thalamus import Thalamus
# from MongoBot.broca import Broca
from MongoBot.hyperthymesia import load_config

logger = logging.getLogger(__name__)


class Medulla(object):
    """
    The medulla oblongata (or medulla) is located in the brainstem, anterior to
    the cerebellum. It is a cone-shaped neuronal mass responsible for autonomic
    (involuntary) functions ranging from vomiting to sneezing. The medulla
    contains the cardiac, respiratory, vomiting and vasomotor centers and
    therefore deals with the autonomic functions of breathing, heart rate and
    blood pressure.

    Mongo's Medulla makes him what he is. Don't fuck with Mongo.
    """

    def __init__(self):

        logger.info('* Becoming self-aware')

        # Remember all the things you were programmed to remember
        self.settings = load_config('config/settings.yaml')
        self.secrets = load_config('config/secrets.yaml')

        # Reach out and touch someone
        self.thalamus = Thalamus()

        # Load the brainmeats
        self.cortex = Cortex(self.thalamus)

        # You are alive. No wait. No you aren't. Not yet at least.
        self.alive = False

    def activate(self):

        logger.info('* Assembling brainmeats')
        self.cortex.init_brainmeats()

        logger.info('* Connecting nuclei')
        self.thalamus.connect()

        logger.info('* Activating Skynet')
        self.alive = True

        while True:
            self.thalamus.process()
