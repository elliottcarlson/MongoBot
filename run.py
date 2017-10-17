#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import coverage
import logging
import logging.config
import os
import sys
import traceback
import unittest

from MongoBot import settings
from MongoBot.medulla import Medulla


def testMongoBot():
    logging.disable(logging.CRITICAL)
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='./tests', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


def runMongoBot(enabled=[], disabled=[]):
    medulla = Medulla(enabled, disabled)
    medulla.activate()


if __name__ == '__main__':  # pragma: no cover
    logconfig = {
        'format': '[%(asctime)s] - %(name)s - %(levelname)s - %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.DEBUG if settings.DEBUG else logging.DEBUG,
        'stream': sys.stdout,
    }
    logging.basicConfig(**logconfig)

    parser = argparse.ArgumentParser()
    parser.add_argument('--test',
                        dest='test',
                        action='store_const',
                        const=1,
                        help='Run unit tests')

    parser.add_argument('--coverage',
                        dest='coverage',
                        action='store_const',
                        const=1,
                        help='Enable test coverage reporting')

    parser.add_argument('--enable',
                        dest='enabled',
                        default=[],
                        action='append',
                        metavar='glossolalia',
                        help='Manually enable specified glossolalia')

    parser.add_argument('--disable',
                        dest='disabled',
                        default=[],
                        action='append',
                        metavar='glossolalia',
                        help='Manually disable specified glossolalia')

    result = parser.parse_args()

    if result.coverage:
        result.test = 1

    if result.test:
        if result.coverage:
            cov = coverage.Coverage()
            cov.start()
            cov.exclude("#pragma: no cover")

        tests = testMongoBot()

        if result.coverage:
            cov.stop()
            cov.save()
            cov.report()

        os._exit(not tests.wasSuccessful())

    else:
        try:
            runMongoBot(result.enabled, result.disabled)
        except:
            traceback.print_exc(file=sys.stdout)
        finally:
            os._exit(0)
