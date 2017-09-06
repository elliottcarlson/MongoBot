# -*- coding: utf-8 -*-
import logging
import math
import re

from MongoBot.autonomic import axon, help
from MongoBot.staff.browser import Browser
from MongoBot.staff.oracle import Oracle

logger = logging.getLogger(__name__)


class Reference(object):

    safe_func = [
        ('abs', abs),
        ('acos', math.acos),
        ('asin', math.asin),
        ('atan', math.atan),
        ('atan2', math.atan2),
        ('ceil', math.ceil),
        ('cos', math.cos),
        ('cosh', math.cosh),
        ('degrees', math.degrees),
        ('e', math.e),
        ('exp', math.exp),
        ('fabs', math.fabs),
        ('floor', math.floor),
        ('fmod', math.fmod),
        ('frexp', math.frexp),
        ('hypot', math.hypot),
        ('ldexp', math.ldexp),
        ('log', math.log),
        ('log10', math.log10),
        ('modf', math.modf),
        ('pi', math.pi),
        ('pow', math.pow),
        ('radians', math.radians),
        ('sin', math.sin),
        ('sinh', math.sinh),
        ('sqrt', math.sqrt),
        ('tan', math.tan),
        ('tanh', math.tanh),
    ]

    safe_calc = dict([(k, locals().get(k, f)) for k, f in safe_func])

    @axon('is.?it.?down')
    def is_it_down(self):
        if not self.stdin:
            return 'Is what down?'

        try:
            url = 'http://downforeveryoneorjustme.com/%s' % self.stdin
            res = Browser(url)

            if re.search('looks down from here', res.read(), re.MULTILINE):
                status = '%s is down' % self.stdin
            else:
                status = '%s is up' % self.stdin

            return status
        except Exception as e:
            logger.exception(e)
            return ('downforeveryoneorjustme.com might be down for everyone...'
                    'or just me?')

    @axon
    @help(('EQUATION <run simple equation in python>, OR ruthlessly fuck with '
           'bot\'s codebase.'))
    def hack(self):
        if not self.values:
            printout = []
            for n, f in self.safe_func:
                if f is not None:
                    printout.append(n)

            return 'Available functions: %s' % ', '.join(printout)

        string = ' '.join(self.values)

        if string.replace(' ', '') == '6*9':
            return '42'

        # This is to stop future Kens
        if '__' in string:
            return 'Rejected.'

        try:
            val = eval(string, {'__builtins__': None}, self.safe_calc)
            result = '{:,}'.format(val)
        except (TypeError, ValueError) as e:
            try:
                result = eval(string, {'__builtins__': None}, self.safe_calc)
            except:
                result = str(e)
        except Exception as e:
            logger.exception(e)
            self.act('not smart enough to do that.')
            return

        return str(result)

    @axon
    @help('WORD [WHICH_DEFINITION] <look up etymology of word>')
    def ety(self):
        """
        I don't remember why this got added, but it's unfailingly awesome.
        """
        try:
            word = self.values[0]
        except:
            return 'Find the etymology of what?'

        try:
            return Oracle(word).etymology()
        except:
            return 'Could not find the etymology for %s' % word
