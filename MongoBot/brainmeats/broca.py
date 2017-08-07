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
        """
        This is where all the conversational tics and automatic reactions are
        set up. Also, for some reason, the mom log, because it's awesome. Is
        the name in poor taste? Yes.
        """

        sentence = data['data']

        if sentence.lower().find('oh snap') != -1:
            self.chat('yeah WHAT?? Oh yes he DID')
            return

        if sentence.lower() == 'boom':
            self.chat(u'(\u2022_\u2022)')
            self.chat(u'( \u2022_\u2022)>\u2310 \u25A1-\u25A1')
            self.chat(u'(\u2310 \u25A1_\u25A1)')
            return

        print('POOP')
