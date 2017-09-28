# -*- coding: utf-8 -*-
import logging
import textwrap

from MongoBot.dendrite import dendrate, Dendrite
from MongoBot.hyperthymesia import load_config
from MongoBot.neuroplasticity import Neuroplasticity
from MongoBot.wernicke import Wernicke

logger = logging.getLogger(__name__)


class Cortex(object):
    """
    The cerebral cortex is the outer layer of neural tissue of the cerebrum of
    the brain, in humans and other mammals. It is separated into two cortices,
    by the longitudinal fissure that divides the cerebrum into the left and
    right cerebral hemispheres. The two heimsphers are joined beneath the
    cortex by the corpus callosum. The cerebral cortex plays a key role in
    memory, attention, perception, awareness, thought, language, and
    consciousness. Humans have around 25 billion neurons in the cerebral
    cortex, almost as many as elephants but substantially less than dolphins,
    pilot and killer whales.

    Basically, all the interesting interactions stem from the cortex, as it
    parses incoming commands from the thalamus and processes them with
    brainmeats.
    """
    cortical_map = {}
    thalamus = {}
    wernicke = None

    def __init__(self, thalamus):

        Cortex.settings = load_config('./config/settings.yaml')
        command_prefix = Cortex.settings.general.get('command_prefix', '.')
        multi_prefix = Cortex.settings.general.get('multi_prefix', ':')

        Cortex.cortical_map = Neuroplasticity()
        Cortex.cortical_map.initialize()

        Cortex.thalamus = thalamus

        Cortex.wernicke = Wernicke(
            command_prefix=command_prefix,
            multi_prefix=multi_prefix
        )

    @staticmethod
    def comprehend(incoming):
        incoming['stdin'] = None

        actions = Cortex.wernicke.parse(incoming.get('data'))
        env = None
        response = None

        if not actions:
            return

        for action in actions:
            (prefix, command) = action.pop(0)[:2]
            parameters = action.pop() if len(action) else []
            command = Cortex.cortical_map.get(command)

            if not command:
                return

            if prefix == Cortex.settings.general.get('command_prefix', '.'):
                if response:
                    incoming['stdin'] = response

                    if not parameters:
                        parameters = response.split()
                else:
                    incoming['stdin'] = ' '.join([str(x) for x in parameters])

                try:
                    print(command)
                    env = Dendrite(incoming, parameters, Cortex.thalamus)
                    instance = dendrate(env, command[0])()
                    mod = getattr(instance, command[1])
                    response = mod()

                    del instance
                    del mod
                except Exception as e:
                    logger.exception('Error running brainmeats: %s', e)
            elif prefix == Cortex.settings.general.get('multi_prefix', ':'):
                for parameter in parameters:
                    incoming['stdin'] = parameter

                    env = Dendrite(incoming, parameter, Cortex.thalamus)
                    instance = dendrate(env, command[0])()
                    mod = getattr(instance, command[1])
                    env.chat(mod())

                    del instance
                    del mod
                return
        # try:
        response = textwrap.wrap(response, 300)

        if isinstance(response, list):
            for line in response:
                env.chat(line)
        else:
            env.chat(response)
        # except Exception as e:
        #     logger.warn('Unable to send response: %s', e)

    def brain_dead(self):
        self.cortical_map.stop()
