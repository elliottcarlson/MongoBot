# -*- coding: utf-8 -*-

import logging
import re
from MongoBot.utils import yo_dawg
from MongoBot.cortex import Cortex

logger = logging.getLogger(__name__)


@yo_dawg
def axon(func, *args, **kwargs):
    func.create_command = True

    if args:
        Cortex.brainmeats['regex'][re.compile(*args)] = func
    else:
        Cortex.brainmeats['plain'][func.__name__] = func

    return func




def caxon(func, *args, **kwargs):
    func.create_command = True
    return func

class baxon(object):
    def __init__(self, func, obj=None, cls=None, method_type='function'):
        self.func = func
        self.obj = obj
        self.cls = cls
        self.method_type = method_type
        self.create_command = True

        Cortex.brainmeats[func.__name__] = func

    def __get__(self, obj=None, cls=None):
        if self.obj == obj and self.cls:
            return self

        method_type = (
            'staticmethod' if isinstance(self.func, staticmethod) else
            'classmethod' if isinstance(self.func, classmethod) else
            'instancemethod'
        )

        return object.__getattribute__(self, '__class__')(
            self.func.__get__(obj, cls), obj, cls, method_type
        )

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __getattribute__(self, attr_name):
        if attr_name in ('__init__', '__get__', '__call__', '__getattribute__',
                         'func', 'obj', 'cls', 'method_type'):
            return object.__getattribute__(self, attr_name)

        return getattr(self.func, attr_name)

    def __repr__(self):
        return self.func.__repr__()
