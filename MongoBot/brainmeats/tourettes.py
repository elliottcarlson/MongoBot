# -*- coding: utf-8 -*-
import logging

from MongoBot.hyperthymesia import load_config
from MongoBot.synapses import Cerebellum, Receptor
from random import choice

logger = logging.getLogger(__name__)


@Cerebellum
class Tourettes(object):
    """
    This is where all the conversational tics and automatic reactions are
    set up. Also, for some reason, the mom log, because it's awesome. Is
    the name in poor taste? Yes.
    """
    config = load_config('config/tourettes.yaml')

    @Receptor('overheard')
    def tourettes(self, incoming):
        message = incoming.stdin

        if message.lower().find('oh snap') != -1:
            incoming.chat('yeah WHAT?? Oh yes he DID')
            return

        if message.lower() == 'boom':
            incoming.chat(u'(\u2022_\u2022)')
            incoming.chat(u'( \u2022_\u2022)>\u2310 \u25A1-\u25A1')
            incoming.chat(u'(\u2310 \u25A1_\u25A1)')
            return

        if message.lower() == 'sup':
            incoming.chat('chillin')
            return

        if message.lower().find('murica') != -1:
            incoming.chat('fuck yeah')
            return

        if message.lower().find('hail satan') != -1:
            incoming.chat(u'\u26E7\u26E7\u26E7\u26E7\u26E7')
            return

        if message.lower().find('race condition') != -1:
            incoming.chat('It\'s never a race condition.')
            return

        if message.lower().find('rimshot') != -1:
            incoming.chat('*ting*')
            return

        if message.lower().endswith('stop'):
            incoming.chat(choice(Tourettes.config.get('stops')))
            return

        if message.lower().find("idk") != -1:
            incoming.chat((u'\u00AF\u005C\u005F\u0028\u30C4'
                           u'\u0029\u005F\u002F\u00AF'))
            return

        if (message.lower().strip() in Tourettes.config.frustration or
           message.lower().find('stupid') == 0):
            incoming.chat((u'\u0028\u256F\u00B0\u25A1\u00B0\uFF09'
                           u'\u256F\uFE35\u0020\u253B\u2501\u253B'))
            return

        if message.strip() in Tourettes.config.wrong_window:
            incoming.chat('Wrong window.')
            return

        inquiries = [message.lower().find(t) != -1 for t in Tourettes.config.questions]

        if Tourettes.config.smartass and True in inquiries:
            smartassery = message.lower().split(Tourettes.config.questions[inquiries.index(True)])[1]
            responses = Tourettes.config.ithelp

            # Dynamic cases need to be appended
            lmgtfy = 'http://lmgtfy.com/?q=' + smartassery.replace(' ', '+')
            responses.append(lmgtfy)

            incoming.chat(choice(responses))
            return

        # There's a very good reason for this.
        if (message == 'oh shit its your birthday erikbeta happy birthday' and
           incoming.source == 'jcb'):
            incoming.act(" slaps jcb")
            incoming.chat("LEAVE ERIK ALONE!")
            return
