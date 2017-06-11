# -*- coding: utf-8 -*-

import inspect
import logging
import os
import sys
import traceback
from glob import glob
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
        'regex': {},
        'class': {}
    }
    wernicke = Wernicke()
    thalamus = None

    def __init__(self, thalamus):
        Cortex.thalamus = thalamus

    def init_brainmeats(self):

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
            module_list = [os.path.split(f)[-1][:-3] for f in module_list]

        for module in module_list:

            try:
                logger.info('Loading brainmeat "%s"', module)

                mod = __import__(brainmeat, fromlist=[module])

                mod = getattr(mod, module)
                cls = getattr(mod, module.capitalize())

                instance = cls()
                methods = inspect.getmembers(instance)

                for name, m in methods:
                    if not hasattr(m, 'axon'):
                        continue

                    Cortex.brainmeats[m.axon_type][m.axon] = (cls, m.__name__)
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

        # Don't ask. It made sense to do this at the time. - E.
        def mixin(cls, target):
            class_name = '%sMixIn' % cls.__class__.__name__

            def __init__(self, *args, **kwargs):
                self.__bound_instance__ = cls

            methods = {}
            for member in inspect.getmembers(cls):
                if inspect.ismethod(member[1]):
                    def __bound_call__(self, *args, **kwargs):
                        mod = getattr(self.__bound_instance__, member[0])
                        if callable(mod):
                            mod(*args, **kwargs)
                        else:
                            return mod

                    __bound_call__.__name__ = member[0]
                    methods[member[0]] = __bound_call__
                elif not callable(member[1]) and not member[0].startswith('_'):
                    methods[member[0]] = member[1]

            methods['__init__'] = __init__

            return type(class_name, (target,), methods)

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

                try:
                    env = Dendrite(incoming, parameters, Cortex.thalamus)

                    # Sure; let's try to mixin a class and classinstance...
                    instance = mixin(env, command[0])()
                    mod = getattr(instance, command[1])

                    response = mod()

                    # So damn important...
                    del instance
                    del mod

                except Exception as e:
                    logger.warn('Error running brainmeats: %s', e)
                    traceback.print_exc(sys.exc_info())

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
