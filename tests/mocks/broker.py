# -*- coding: utf-8 -*-
class MockBroker(object):
    """
    A mock class to handle unit tests that utilize Broker
    """
    def __init__(self, symbol):
        self.symbol = symbol

        if not symbol:
            return

    def showquote(self):
        if self.symbol == 'GOOG':
            return 'Alphabet Inc. (GOOG), 914.39, ${green:7.15 (0.79%)}, http://roa.st/cok'

        if self.symbol == 'INVALID':
            return 'Couldn\'t find company: INVALID'

        return False
