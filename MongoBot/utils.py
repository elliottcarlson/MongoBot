# -*- coding: utf-8 -*-

import logging
import random
import time
from functools import wraps

logger = logging.getLogger(__name__)


# http://stackoverflow.com/questions/667508/whats-a-good-rate-limiting-algorithm
def ratelimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)

    def decorate(func):
        lastTimeCalled = [0.0]

        def rateLimitedFunction(*args, **kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait > 0:
                time.sleep(leftToWait)
            ret = func(*args, **kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rateLimitedFunction
    return decorate


def yo_dawg(func):
    """
    Yo dawg, I heard you wanted to decorate your decorators, allowing your
    decorator to be used with or without arguments:
    @decorator(with, arguments, and=kwargs)
    or
    @decorator
    """
    @wraps(func)
    def yo_dawg(*args, **kwargs):

        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return func(args[0])
        else:
            return lambda yo_func: func(yo_func, *args, **kwargs)

    return yo_dawg


def aphasia(func):
    def wrapper(cls, message):
        try:
            rand = random.randint(1, 170)

            if rand == 13:
                message = zalgo(message)
            elif rand == 23:
                i = message.split()
                pos = random.randint(0, len(i))
                i.insert(pos, 'fnord')
                message = ' '.join(i)
        except Exception as e:
            logger.debug('Error applying aphasia: %s' % e)
            print(e)
            pass

        return func(cls, message)

    return wrapper


zalgochars = [
    [
        u'\u030d',       u'\u030e',       u'\u0304',       u'\u0305',
        u'\u033f',       u'\u0311',       u'\u0306',       u'\u0310',
        u'\u0352',       u'\u0357',       u'\u0351',       u'\u0307',
        u'\u0308',       u'\u030a',       u'\u0342',       u'\u0343',
        u'\u0344',       u'\u034a',       u'\u034b',       u'\u034c',
        u'\u0303',       u'\u0302',       u'\u030c',       u'\u0350',
        u'\u0300',       u'\u0301',       u'\u030b',       u'\u030f',
        u'\u0312',       u'\u0313',       u'\u0314',       u'\u033d',
        u'\u0309',       u'\u0363',       u'\u0364',       u'\u0365',
        u'\u0366',       u'\u0367',       u'\u0368',       u'\u0369',
        u'\u036a',       u'\u036b',       u'\u036c',       u'\u036d',
        u'\u036e',       u'\u036f',       u'\u033e',       u'\u035b',
        u'\u0346',       u'\u031a'
    ],

    [
        u'\u0316',       u'\u0317',       u'\u0318',       u'\u0319',
        u'\u031c',       u'\u031d',       u'\u031e',       u'\u031f',
        u'\u0320',       u'\u0324',       u'\u0325',       u'\u0326',
        u'\u0329',       u'\u032a',       u'\u032b',       u'\u032c',
        u'\u032d',       u'\u032e',       u'\u032f',       u'\u0330',
        u'\u0331',       u'\u0332',       u'\u0333',       u'\u0339',
        u'\u033a',       u'\u033b',       u'\u033c',       u'\u0345',
        u'\u0347',       u'\u0348',       u'\u0349',       u'\u034d',
        u'\u034e',       u'\u0353',       u'\u0354',       u'\u0355',
        u'\u0356',       u'\u0359',       u'\u035a',       u'\u0323'
    ],

    [
        u'\u0315',       u'\u031b',       u'\u0340',       u'\u0341',
        u'\u0358',       u'\u0321',       u'\u0322',       u'\u0327',
        u'\u0328',       u'\u0334',       u'\u0335',       u'\u0336',
        u'\u034f',       u'\u035c',       u'\u035d',       u'\u035e',
        u'\u035f',       u'\u0360',       u'\u0362',       u'\u0338',
        u'\u0337',       u'\u0361',       u'\u0489'
    ],
]

fears = [
    'HE COMES',
    'they are coming',
    'cannot see',
    'she is glorious',
    'no hope no hope',
    'it rises',
    'no light',
    'no escape',
    'breaking',
    'in my mind',
    'pain',
    'cannot move',
    'nightmares',
    'a room with a moose',
]


def zalgo(_string):

    if len(_string) < 10:
        return _string

    amount = random.randint(10, len(_string))
    base = _string[:amount]
    zalgoit = list(_string[amount:])
    zalgoed = u''
    while zalgoit:
        # TODO Not sure if all the incessant u''ing is necessary
        char = zalgoit.pop(0)
        zalgoed = u'%s%s' % (zalgoed, char)

        if char == ' ':
            continue

        if random.randint(0, 30) == 13:
            fear = ' %s' % random.choice(fears)
            zalgoit = list(fear) + zalgoit
            continue

        direction = random.choice(zalgochars)
        for x in range(0, 4):
            tic = random.choice(direction)
            zalgoed = u'%s%s' % (zalgoed, tic)

    return u'%s%s' % (base, zalgoed)


def test():
    print('??')
