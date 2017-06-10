#!/usr/bin/env python

import sys
import logging
import logging.config
from MongoBot import settings
from MongoBot.medulla import Medulla


def main():
    kw = {
        'format': '[%(asctime)s] - %(name)s - %(levelname)s - %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.DEBUG if settings.DEBUG else logging.INFO,
        'stream': sys.stdout,
    }
    logging.basicConfig(**kw)

    medulla = Medulla()
    medulla.activate()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
