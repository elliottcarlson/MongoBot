#! -*- coding: utf-8 -*-
import mock
import unittest

from MongoBot.medulla import Medulla


class TestMedulla(unittest.TestCase):
    @mock.patch('MongoBot.medulla.Thalamus')
    @mock.patch('MongoBot.medulla.Cortex')
    def test_init(self, mock_cortex, mock_thalamus):
        medulla = Medulla()

        self.assertIsInstance(medulla, Medulla)
        mock_thalamus.assert_called()
        mock_cortex.assert_called()

    @mock.patch('MongoBot.medulla.Thalamus')
    @mock.patch('MongoBot.medulla.Cortex')
    def test_activate(self, mock_cortex, mock_thalamus):
        mock_thalamus.return_value.process.side_effect = Exception

        medulla = Medulla()

        # We expect an exception that breaks the endless loop in activate()
        with self.assertRaises(Exception):
            medulla.activate()
