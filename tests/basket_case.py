# -*- coding: utf-8 -*-
import os
import unittest

from MongoBot.hyperthymesia import load_config


def should_be_axon(func):
    """
    Decorator to check that method is an axon. Only use it on a test method
    using the naming convention of test_<method to test>().

    Usage:

        @_should_be_axon
        def test_advice(self):
            ...
    """
    def check(self):
        func_name = func.__name__.split('test_', 1)[1]
        func_root = getattr(self.instance, func_name)
        self.assertTrue(hasattr(func_root, 'axon'))
        func(self)

    return check


class BasketCase(unittest.TestCase):
    """
    A base unit testing class for brainmeats that implements required
    functionality that Dendrite usually provides.
    """

    def setUpInstance(self, cls):
        self.instance = cls()
        self._mock_state = {}
        self._mocks = {}

        self.instance.values = []
        self.instance.stdin = None
        self.instance.source = 'TestRunner'

        self._mocks['chat'] = False
        self._mock_chats = []
        self.instance.chat = self._mock_chat

        self._mocks['act'] = False
        self._mock_actions = []
        self.instance.act = self._mock_act

        self.instance.get = self._mock_get
        self.instance.set = self._mock_set

        config_file = './config/%s.yaml' % cls.__name__.lower()
        if os.path.isfile(config_file):
            self.instance.config = load_config(config_file)

        self.instance.settings = load_config('./config/settings.yaml')

    def _mock_act(self, action):
        """
        Register when self.act() is called from a brainmeats.
        """
        self._mocks['act'] = True
        self._mock_actions.append(action)

    def assertActed(self, action=None):
        if action:
            self.assertTrue(action in self._mock_actions)
        else:
            self.assertTrue(self._mocks['act'])

    def assertNotActed(self, action=None):
        if action:
            self.assertFalse(action in self._mock_actions)
        else:
            self.assertFalse(self._mocks['act'])

    def _mock_chat(self, message):
        """
        Register when self.chat() is called from a brainmeats.
        """
        self._mocks['chat'] = True
        self._mock_chats.append(message)

    def assertChatted(self, message=None):
        if message:
            self.assertTrue(message in self._mock_chats)
        else:
            self.assertTrue(self._mocks['chat'])

    def assertNotChatted(self, message=None):
        if message:
            self.assertFalse(message in self._mock_chats)
        else:
            self.assertFalse(self._mocks['chat'])

    def _mock_get(self, key, default=None):
        return self._mock_state.get(key, default)

    def _mock_set(self, key, value):
        return self._mock_state.update({key: value})
