# -*- coding: utf-8 -*-
from __future__ import absolute_import
import imp
import importlib
import logging
import re
import sys
import time
from glob import glob
from six.moves import _thread
from MongoBot import settings
from MongoBot.corpuscallosum import CorpusCallosum
#from MongoBot.cortex import Cortex
from MongoBot.thalamus import Thalamus
#from MongoBot.broca import Broca
#from MongoBot.hyperthymesia import Hyperthymesia

logger = logging.getLogger(__name__)

"""
The medulla oblongata (or medulla) is located in the brainstem, anterior to the
cerebellum. It is a cone-shaped neuronal mass responsible for autonomic
(involuntary) functions ranging from vomiting to sneezing. The medulla contains
the cardiac, respiratory, vomiting and vasomotor centers and therefore deals
with the autonomic functions of breathing, heart rate and blood pressure.
"""
class Medulla(object):

    def __init__(self):

        self.corpuscallosum = CorpusCallosum()

        self.thalamus = Thalamus()

        print('* Becoming self-aware')
        #self._settings = load_config('config/settings.yaml')
        #self._secrets = load_config('config/secrets.yaml')
        self.alive = False





        """
        try:
            self.brain = Cortex(self)
        except Exception as e:
            logger.warn('Drain bamaged... Stroking... out...')
            sys.exit()




        self.brain = Cortex(self)
        self.thalamus = Thalamus(self, self.brain)
        """

    def rise(self):

        print('* Assembling brainmeats')
        self.corpuscallosum.init_brainmeats()

        print('* Triggering brain waves')
        self.thalamus.connect()


        while True:
            self.thalamus.process()
