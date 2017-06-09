# -*- coding: utf-8 -*-

import copy
import logging
import yaml
from collections import OrderedDict, Sequence, Mapping
from os import path, listdir

logger = logging.getLogger(__name__)


class Hyperthymesia(yaml.Loader):
    """
    Hyperthymesia is the condition of possessing an extremely detailed
    autobiographical memory. People with hyperthymesia remember an abnormally
    vast number of their life experiences.

    It's also a great term to use for managing configuration states.
    """
    eidetic = dict()

    def __init__(self, stream):

        self._root = path.split(stream.name)[0]
        super(Hyperthymesia, self).__init__(stream)

    def include(self, node):

        filepath = path.join(self._root, self.construct_scalar(node))
        if path.isdir(filepath):
            for filename in listdir(filepath):
                if path.isfile(filename):
                    return self.load(filename)
        else:
            return self.load(filepath)

    def sequence(self, node):

        return YamlList(self.construct_object(child) for child in node.value)

    def mapping(self, node):

        make_obj = self.construct_object

        return YamlDict((make_obj(k), make_obj(v)) for k, v in node.value)

    def load(self, path):

        if path not in self.eidetic:
            with open(path, 'r') as stream:
                self.eidetic.update({path: yaml.load(stream, Hyperthymesia)})

        return self.eidetic.get(path, dict())


class YamlDict(OrderedDict):

    def __init__(self, *args, **kwargs):
        super(YamlDict, self).__init__(*args, **kwargs)
        self.__root = self

    def __getattr__(self, key):
        if key in self:
            return self[key]

        return super(YamlDict, self).__getattribute__(key)

    def __getitem__(self, key):
        v = super(YamlDict, self).__getitem__(key)

        if isinstance(v, basestring):
            v = v.format(**self.__root)

        return v

    def __setitem__(self, key, value):

        if isinstance(value, Mapping) and not isinstance(value, YamlDict):
            value = YamlDict(value)
        elif isinstance(value, basestring):
            pass
        elif isinstance(value, Sequence) and not isinstance(value, YamlList):
            value = YamlList(value)

        super(YamlDict, self).__setitem__(key, value)

    def copy(self):

        return copy.deepcopy(self)

    def setAsRoot(self, root=None):
        if root is None:
            root = self

        self.__root = root

        for k, v in self.iteritems():
            if hasattr(v, 'setAsRoot'):
                v.setAsRoot(root)


class YamlList(list):

    ROOT_NAME = 'root'

    def __init__(self, *args, **kwargs):
        super(YamlList, self).__init__(*args, **kwargs)
        self.__root = {YamlList.ROOT_NAME: self}

    def __getitem__(self, key):
        v = super(YamlList, self).__getitem__(key)
        if isinstance(v, basestring):
            v = v.format(**self.__root)

        return v

    def __setitem__(self, key, value):

        if isinstance(value, Mapping) and not isinstance(value, YamlDict):
            value = YamlDict(value)
        elif isinstance(value, Sequence) and not isinstance(value, YamlList):
            value = YamlList(value)

        super(YamlList, self).__setitem__(key, value)

    def copy(self, *args):
        return copy.deepcopy(self)

    def setAsRoot(self, root=None):
        if root is None:
            root = {YamlList.ROOT_NAME: self}

        self.__root = root

        for v in self:
            if hasattr(v, 'setAsRoot'):
                v.setAsRoot(root)


def load_config(config_file):
    try:
        stream = file(config_file, 'r')

        data = yaml.load(stream, Hyperthymesia)

        if data is not None:
            data.setAsRoot()

        return data

    except Exception as e:
        logger.warn('load_config error: %s', e)
        pass

Hyperthymesia.add_constructor('!include', Hyperthymesia.include)
Hyperthymesia.add_constructor(u'tag:yaml.org,2002:seq', Hyperthymesia.sequence)
Hyperthymesia.add_constructor(u'tag:yaml.org,2002:map', Hyperthymesia.mapping)
