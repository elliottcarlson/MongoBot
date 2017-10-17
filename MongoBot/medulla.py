# -*- coding: utf-8 -*-
import logging

from MongoBot.cortex import Cortex
from MongoBot.thalamus import Thalamus

logger = logging.getLogger(__name__)


class Medulla(object):
    """
    The medulla oblongata (or medulla) is located in the brainstem, anterior to
    the cerebellum. It is a cone-shaped neuronal mass responsible for autonomic
    (involuntary) functions ranging from vomiting to sneezing. The medulla
    contains the cardiac, respiratory, comiting and vasomotor centers and
    therefore deals with the autonomic functions of breathing, heart rate and
    blood pressue.

    Mongo's medulla makes him what he is. Don't fuck with Mongo.
    """

    def __init__(self, enabled=[], disabled=[]):
        logger.info('Becoming self-aware.')

        self.thalamus = Thalamus(enabled, disabled)

        logger.info('* Assembling brainmeats')
        self.cortex = Cortex(self.thalamus)

        self.alive = False

    def activate(self):

        logger.info('* Activating Skynet')
        self.alive = True

        logger.info('* Connecting nuclei')
        self.thalamus.connect()
