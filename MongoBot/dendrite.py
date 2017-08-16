# -*- coding: utf-8 -*-
import inspect
import os.path
import re

from MongoBot.hyperthymesia import load_config
from MongoBot.utils import aphasia


def dendrate(cls, target):
    """
    dendrate is like hydrating a class with dendrites...

    yeah that makes sense.

    trust me.

    Basically, we can allow brainmeats to be completely autonomous from the
    rest of Mongo - we build a mix-in class from Dendrite and the brainmeat we
    are loading in, that dendrates the brainmeat with functionality from
    Dendrite - no need to maintain information of the service that the request
    came from within the brainmeat.

    This made sense to me at the time.
    """
    class_name = '%sMixIn' % cls.__class__.__name__

    def __init__(self, *args, **kwargs):
        self.__bound_instance__ = cls

    methods = {}
    for member in inspect.getmembers(cls):
        if inspect.ismethod(member[1]):
            methods[member[0]] = getattr(cls, member[0])
        elif not callable(member[1]) and not member[0].startswith('_'):
            methods[member[0]] = member[1]

    methods['__init__'] = __init__

    # If a config file exists for the brainmeats, load it in and make it
    # available as self.config
    config_file = './config/%s.yaml' % target.__name__.lower()
    if os.path.isfile(config_file):
        methods['config'] = load_config(config_file)

    # Make the global config available to the brainmeats
    methods['settings'] = load_config('./config/settings.yaml')

    return type(class_name, (target,), methods)


class Dendrite(object):

    _state = {}

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

        self.link = self.thalamus.providers[self.provider]

    @aphasia
    def chat(self, message):
        self.link.chat(self.colorize(message), target=self.target)

    def colorize(self, text):
        """
        Outbound messages can have colorization applied to elements, if the
        protocol allows for it.

        Colorized text needs to be formated with a ${color_name:text} format,
        and the protocol needs to have a method named colorize that can
        transform that in to the appropriate color code. If the protocol does
        not support colorization, and does not have a colorize method, it will
        automatically strip the colorization code and only display the raw
        text.
        """
        def no_color(text, color):
            return text

        colorizer = getattr(self.link, 'colorize', no_color)

        def do_colorization(match):
            match = match.group(1)
            color, text = match.split(':', 1)
            return colorizer(text, color)

        return re.sub(r'\${((\w+):(.*?))}', do_colorization, text)

    def get(self, key, default=None):
        print(Dendrite._state)
        return Dendrite._state.get(key, default)

    def set(self, key, value):
        Dendrite._state.update({ key: value })
