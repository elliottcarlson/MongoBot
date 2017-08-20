# -*- coding: utf-8 *-*


class MockIncomingDendrite(object):
    def __init__(self, stdin, source=None):
        self.stdin = stdin
        self.source = source

        self.chats = []
        self.acts = []

    def chat(self, msg):
        self.chats.append(msg)

    def act(self, msg):
        self.acts.append(msg)
