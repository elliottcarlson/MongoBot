# -*- coding: utf-8 -*-

import re
from MongoBot.autonomic import axon

@axon
def test1():
    pass

@axon('what')
def test2():
    pass

@axon('hello$', re.IGNORECASE)
def test3():
    pass

