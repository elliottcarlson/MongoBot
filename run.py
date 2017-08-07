#!/usr/bin/env python
import sys
import logging
import logging.config
import os

from MongoBot import settings
from MongoBot.medulla import Medulla


def main():
    logconfig = {
        'format': '[%(asctime)s] - %(name)s - %(levelname)s - %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.DEBUG if settings.DEBUG else logging.DEBUG,
        'stream': sys.stdout,
    }
    logging.basicConfig(**logconfig)

    medulla = Medulla()
    medulla.activate()

if __name__ == '__main__':  # pargma: no cover
    try:
        main()
    except KeyboardInterrupt:
        os._exit(0)
