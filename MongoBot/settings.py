# -*- coding: utf-8 -*-
import os

DEBUG = False

BRAINMEATS = [
    'MongoBot.brainmeats',
]

ERRORS_TO = 'sublimnl'

for key in os.environ:
    if key[:9] == 'MONGOBOT_':
        name = key[9:]
        globals()[name] = os.environ[key]
