# -*- coding: utf-8 -*-

import os
import logging
from glob import glob
from six import PY2
from importlib import import_module
from MongoBot import settings
from MongoBot.utils import to_utf8

logger = logging.getLogger(__name__)


class CorpusCallosum(object):
    """
    The corpus callosum is a wide, flat bundle of neural fibers about 10 cm
    long beneath the cortex in the eutherian brain at the longitudinal fissure.
    It connects the left and right cerebral hemispheres and facilitates
    interhemispheric communication. It is the largest white matter structure in
    the brain, consisting of 200-250 million contralateral axonal projections.

    In MongoBot, the Corpus Callosum finds and holds the brainmeats together.
    """

    def __init__(self):
        pass

    commands = {
        'respond_to': {},
        'listen_to': {},
        'default_reply': {},
    }

    def init_brainmeats(self):

        if hasattr(settings, 'BRAINMEATS'):
            brainmeats = settings.BRAINMEATS
        else:
            brainmeats = ['MongoBot.brainmeats']

        for brainmeat in brainmeats:
            self._load_brainmeat(brainmeat)

    def _load_brainmeat(self, brainmeat):

        logger.info('Loading brainmeat "%s"', brainmeat)
        path_name = None

        if PY2:

            import imp

            for mod in brainmeat.split('.'):
                if path_name is not None:

                    path_name = [path_name]

                _, path_name, _ = imp.find_module(mod, path_name)
        else:

            from importlib.util import find_spec as importlib_find

            path_name = importlib_find(brainmeat)

            try:

                path_name = path_name.submodule_search_locations[0]
            except TypeError:

                path_name = path_name.origin

        module_list = [brainmeat]

        if not path_name.endswith('.py'):

            module_list = glob('{}/[!_]*.py'.format(path_name))
            module_list = ['.'.join((brainmeat, os.path.split(f)[-1][:-3])) for
                           f in module_list]

        for module in module_list:

            try:

                logger.info('Loading brainmeat "%s"', module)
                import_module(module)

            except:

                logger.exception('Failed to import "%s"', module)

    def get_brainmeats(self, category, text):

        has_matching_plugin = False

        if text is None:

            text = ''

        for matcher in self.commands[category]:

            m = matcher.search(text)

            if m:

                has_matching_plugin = True
                yield self.commands[category][matcher], to_utf8(m.groups())

        if not has_matching_plugin:

            yield None, None
