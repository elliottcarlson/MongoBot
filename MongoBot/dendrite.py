# -*- coding: utf-8 -*-

from MongoBot.utils import aphasia


class Dendrite(object):

    def __init__(self, incoming, params, thalamus):

        self.thalamus = thalamus

        self.service = incoming['service']
        self.module = incoming['module']
        self.provider = incoming['provider']

        self.target = incoming['target']
        self.source = incoming['source']  # TODO: Implement ID on sources

        self.stdin = incoming.get('stdin')
        self.raw_msg = incoming['data']
        self.values = params

    @aphasia
    def chat(self, message):

        self.thalamus.providers[self.provider].chat(message, self.target)
