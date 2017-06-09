import logging
from logging import config, Handler

class Hyperthymesia(object):
    name = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'error': logging.ERROR,
        'warning': logging.WARNING,
        'critical': logging.CRITICAL
    }

    def __init__(self, *args, **kwargs):
        
        logging.config.dictConfig(settings.logging)


    def __set_log_level(self, level):

        self.logger = logging.getLogger(level)

        try:
            level = self.names[level.lower()]
        except KeyError:
            level = logging.WARNING

        self.logger.setLevel(level)


    def info(self, message):

        self.__set_log_level('info')
        self.logger.info(message)


    def debug(self, message):

        self.__set_log_level('debug')
        self.logger.debug(message)


    def warn(self, message):

        self.__set_log_level('warn')
        self.logger.warn(message)


class ChatHandler(logging.Handler):

    def __init__(self, cortex):

        logging.Handler.__init__(self)
        self.cortex = cortex


    def emit(self, record):

        self.brain.thalamus.send(record)
