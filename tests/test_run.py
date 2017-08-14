import logging
import unittest

from mock import patch
from run import runMongoBot


class TestRunner(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    @patch('MongoBot.medulla.Medulla.activate')
    def test_medulla_activated(self, mock):
        runMongoBot()
        self.assertTrue(mock.called)
