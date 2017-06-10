# -*- coding: utf-8 -*-

import logging
import os
from glob import glob
from importlib import import_module
from MongoBot import settings
from MongoBot.dendrite import Dendrite
from MongoBot.wernicke import Wernicke
from six import PY2

logger = logging.getLogger(__name__)


class Cortex(object):
    """
    The cerebral cortex is the outer layer of neural tissue of the cerebrum of
    the brain, in humans and other mammals. It is separated into two cortices,
    by the longitudinal fissure that divides the cerebrum into the left and
    right cerebral hemispheres. The two hemispheres are joined beneath the
    cortex by the corpus callosum. The cerebral cortex plays a key role in
    memory, attention, perception, awareness, thought, language, and
    consciousness. Humans have around 25 billion neurons in the cerebral
    cortex, almost as many as elephants but substantially less than dolphins,
    pilot and killer whales.

    Basically all the interesting interactions stem from the Cortex, as it
    parses incomming commands and interprets the data with Brainmeats.
    """
    brainmeats = {
        'plain': {},
        'regex': {}
    }
    wernicke = Wernicke()
    thalamus = None

    def __init__(self, thalamus):
        Cortex.thalamus = thalamus

    def init_brainmeats(self):

        if hasattr(settings, 'BRAINMEATS'):
            brainmeats = settings.BRAINMEATS
        else:
            brainmeats = ['MongoBot.brainmeats']

        for brainmeat in brainmeats:
            self._load_brainmeat(brainmeat)

    def _load_brainmeat(self, brainmeat):

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

    @staticmethod
    def get_brainmeats(brainmeat):

        if brainmeat is None:
            brainmeat = ''

        if brainmeat in Cortex.brainmeats['plain']:
            return Cortex.brainmeats['plain'][brainmeat]

        for matcher in Cortex.brainmeats['regex']:
            m = matcher.search(brainmeat)

            if m:
                return Cortex.brainmeats['regex'][matcher]

        return None

    @staticmethod
    def interpret(incoming):

        actions = Cortex.wernicke.parse(incoming.get('data'))
        env = None
        response = None

        if not actions:
            return

        for action in actions:
            prefix, command = action.pop(0)[:2]
            parameters = action.pop() if len(action) else []

            command = Cortex.get_brainmeats(command)

            if not command:
                return

            if prefix == '.':
                if response:
                    incoming['stdin'] = response

                    if not parameters:
                        parameters = response.split()
                else:
                    incoming['stdin'] = ' '.join([str(x) for x in parameters])

                env = Dendrite(incoming, parameters, Cortex.thalamus)
                response = command(env)
            elif prefix == ':':
                for parameter in parameters:
                    incoming['stdin'] = parameter

                    env = Dendrite(incoming, parameter, Cortex.thalamus)
                    env.chat(command(env))

                return

        try:
            env.chat(response)
        except Exception as e:
            logger.warn('Unable to send response: %s', e)
