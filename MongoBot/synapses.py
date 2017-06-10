# -*- coding: utf-8 -*-


class Neurons(object):
    """
    Neurons hold some vesicles. Vesicles are cool. Are you?
    """

    vesicles = {}


def Cerebellum(object):
    """
    The cerebellum is a major feature of the hindbrain of all vertebrates. In
    humans, the cerebellum plays an important role in motor control, and it may
    also be involved in some cognitive functions such as attention and language
    as well as in regulating fear and pleasure responses, but its
    movement-related functions are the most solidly established.

    MongoBot's Cerebellum is a class decorator and is needed to register
    receptors properly.

    Basically, this is a hack -- Python doesn't bind method decorators until
    the class has been defined; by decorating the class, we are able to trigger
    that binding and determine which methods have been decorated as
    listeners/transmitters without the class having been defined. Super hacky,
    super cool.
    """
    for name, method in object.__dict__.iteritems():
        if hasattr(method, 'is_receptor'):

            receptors = Neurons.vesicles.get(method.name, [])
            receptors.append({object.__name__.lower(): method.neuron})
            Neurons.vesicles.update({method.name: receptors})

    return object


class Synapse(Neurons):
    """
    In the nervous system, a synapse is a structure that permits a neuron (or
    nerve cell) to pass an electrical or chemical signal to another neuron.

    MongoBot's Synapse is an event emitting decorator that will fire off a
    Neuron to all Receptors that are listening for the passed keyword.
    """

    def __init__(self, neuron):

        self.neuron = neuron

    def __call__(self, neuron):

        def glutamate(*args, **kwargs):

            neurotransmission = neuron(*args, **kwargs)

            vesicles = self.vesicles.get(self.neuron, [])
            for vesicle in vesicles:
                for name in vesicle:
                    vesicle[name](vesicle, neurotransmission or [])

            return neurotransmission

        return glutamate


def Receptor(name, *args, **kwargs):
    """
    A receptor is a protein molecule that receives and responds to a
    neurotransmitter, or other substance.

    MongoBot's Receptor is an observer decorator that will auto trigger when a
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
