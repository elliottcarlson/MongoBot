# -*- coding: utf-8 -*-

import os

DEBUG = False

Plugins = [
    'MongoBot.plugins',
]

ERRORS_TO = 'sublimnl'

for key in os.environ:
    if key[:9] == 'MONGOBOT_':
        name = key[9:]
        globals()[name] = os.environ[key]

try:
    from mongobot_settings import *
except ImportError:
    try:
        from local_settings import *
    except ImportError:
        pass
