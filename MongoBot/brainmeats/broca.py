# -*- coding: utf-8 -*-

import logging
from MongoBot.synapses import Cerebellum, Receptor

logger = logging.getLogger(__name__)


@Cerebellum
class Broca(object):

    readstuff = False
    knowledge = False
    draft = False

    def __init__(self):
        pass

    @Receptor('THALAMUS_INCOMING_DATA')
    def tourettes(self, data):

        sentence = data['data']




