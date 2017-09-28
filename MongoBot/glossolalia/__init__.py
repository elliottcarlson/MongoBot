# -*- coding: utf-8 -*-
import logging

from logging.handlers import TimedRotatingFileHandler


class GlossolaliaLogger(TimedRotatingFileHandler):
    def __init__(self, name):
        logfile = 'logs/%s.log' % name.split('.')[-1].lower()
        logformat = '[%(asctime)s] %(message)s'

        TimedRotatingFileHandler.__init__(self, logfile, when='midnight')
        self.setFormatter(logging.Formatter(logformat))
