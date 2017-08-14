# -*- coding: utf-8 -*-
class MockBroker(object):

    def __init__(self, symbol):
        print('woo')
        self.symbol = symbol

        if not symbol:
            return

    def showquote(self):

        if not self.stock:
            return False

        if self.stock == 'GOOG':
            return 'Alphabet Inc. (GOOG), 914.39, ${green:7.15 (0.79%)}, http://roa.st/cok'

        if self.stock == 'INVALID':
            return 'Couldn\'t find company: INVALID'
