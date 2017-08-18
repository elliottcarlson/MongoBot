# -*- coding: utf-8 -*-
import logging
import re

from MongoBot.utils import yo_dawg

logger = logging.getLogger(__name__)


@yo_dawg
def axon(func, *args, **kwargs):
    if args:
        args = list(args)
        args[0] = '^%s$' % args[0]
        func.axon = re.compile(*args)
        func.axon_type = 'regex'
    else:
        func.axon = func.__name__
        func.axon_type = 'named'

    return func


def help(text):
    def add(func):
        func.help = text
        return func

    return add
