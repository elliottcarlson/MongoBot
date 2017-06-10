# -*- coding: utf-8 -*-

import re
from MongoBot.autonomic import axon
from MongoBot.dendrite import Dendrite


class Hello(Dendrite):

    def __init__(self):
        pass

    @axon
    def test1(self):
        self.chat('test')
        return 'woo!'

    @axon
    def test2(self):
        if self.stdin:
            msg = self.stdin
        else:
            msg = 'blah'

        return '%s-%s' % (msg, msg)

    @axon('fuck.*', re.IGNORECASE)
    def test3(self):
        return 'YEAH BITCH'
