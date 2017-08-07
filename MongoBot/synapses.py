# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


class Neurons(object):
    """
    Neurons hold some vesicles. Vesicles are cool. Are you?
    """
    vesicles = {}


def Cerebellum(object):
    """
    The cerebellum is a major feature of the hindbrain of all vertebrates. In
    humans, the cerebellum plays an import role in motor control, and it may
    also be involved in some cognitive functions such as attention and language
    as well as in regulating fear and pleasure reposnses, but its
    movement-related functions are the most solidly established.

    Mongo's cerebellum is a class decorator and is needed to register receptors
    properly.

    Basically, this is a hack -- Python doesn't bind method decorators until
    the class has been defined; by decorating the class, we are able to trigger
    that binding and determine which methods have been decorated as
    listeners/transmitters without the class having been defined. Super hacky,
    super cool.
    """
    #for name, method in object.__dict__.iteritems():
    for name in object.__dict__:
        method = object.__dict__[name]
        if hasattr(method, 'is_receptor'):
            receptors = Neurons.vesicles.get(method.name, [])

            if object.__module__.startswith('MongoBot.brainmeats'):
                func = (object, method.neuron.__name__)
            else:
                func = method.neuron

            receptors.append({object.__name__.lower(): func})
            Neurons.vesicles.update({method.name: receptors})

    return object


class Synapse(Neurons):
    """
    In the nervous system, a synpase is a structure that permits a neuron (or
    nerve cell) to pass an electrical or chemical signal to another neuron.

    Mongo's synapse is an event emitting decorator that will fire off a Neuron
    to all Receptors that are listening for the passed keyword. Finding brain
    metaphors for te Observer pattern was almost as fun as making this hack
    work.
    """
    def __init__(self, neuron):
        self.neuron = neuron

    def __call__(self, neuron):
        def glutamate(*args, **kwargs):
            neurotransmission = neuron(*args, **kwargs)

            if neurotransmission:
                vesicles = self.vesicles.get(self.neuron, [])
                for vesicle in vesicles:
                    for name in vesicle:
                        logger.debug('Sending synapse to receptor "%s"', name)

                        if isinstance(vesicle[name], tuple):
                            instance = vesicle[name][0]()
                            mod = getattr(instance, vesicle[name][1])
                            mod.neuron(instance, neurotransmission or [])
                        else:
                            vesicle[name](object, neurotransmission or [])
            return neurotransmission
        return glutamate


def Receptor(name, *args, **kwargs):
    """
    A receptor is a protein molecule that receives and responds to a
    neurotransmitter, or other substance.

    Mongo's Receptor is an observer decorator that will auto trigger when a
    neuron is fired using a keyword the Receptor is listening for.
    """
    class AutoReceptor(Neurons):
        def __init__(self, neuron, name=False):
            self.neuron = neuron
            self.name = name
            self.is_receptor = True

    def glutamate(func, *args, **kwargs):
        return AutoReceptor(func, name)

    return glutamate
