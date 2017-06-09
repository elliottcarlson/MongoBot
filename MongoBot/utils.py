# -*- coding: utf-8 -*-

import os
import logging
import tempfile
import requests
from contextlib import contextmanager
from functools import wraps
from pprint import pprint
from six.moves import _thread, range, queue
import six

logger = logging.getLogger(__name__)


def to_utf8(s):

    """
    Convert a string to utf8. If the argument is an iterable
    (list/tuple/set), then each element of it would be converted instead.

    >>> to_utf8('a')
    'a'
    >>> to_utf8(u'a')
    'a'
    >>> to_utf8([u'a', u'b', u'\u4f60'])
    ['a', 'b', '\\xe4\\xbd\\xa0']
    """

    if six.PY2:
        if isinstance(s, str):
            return s
        elif isinstance(s, unicode):
            return s.encode('utf-8')
        elif isinstance(s, (list, tuple, set)):
            return [to_utf8(v) for v in s]
        else:
            return s
    else:
        return s


def yo_dawg(func):
    """
    Yo dawg, I heard you wanted to decorate your decorators, allowing your
    decorator to be used with or without arguments:
    @decorator(with, arguments, and=kwargs)
    or
    @decorator
    """
    @wraps(func)
    def yo_yo_dawg(*args, **kwargs):
        
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        
            return func(args[0])

        else:

            return lambda yo_func: func(yo_func, *args, **kwargs)

    return yo_yo_dawg
