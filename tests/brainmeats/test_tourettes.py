# -*- coding: utf-8 -*-
import unittest

from MongoBot.brainmeats.tourettes import Tourettes
from MongoBot.synapses import Neurons
from tests.mocks.incoming_dendrite import MockIncomingDendrite


class TestTourettes(unittest.TestCase):

    def setUp(self):
        self.instance = Tourettes()

        # Change multiple responses to only have one response to give.
        Tourettes.config['ithelp'] = ['Are you sure your computer is on?']
        Tourettes.config['stops'] = ['Hammertime']

    def test_Tourettes(self):
        self.assertIsInstance(self.instance, Tourettes)

    def test_tourettes_is_receptor_for_overheard(self):
        self.assertIn('overheard', Neurons.vesicles)
        receptors = set().union(*(d.keys() for d in
                                Neurons.vesicles.get('overheard')))
        self.assertIn('tourettes', receptors)

    def test_tourettes_contains_oh_snap(self):
        dendrite = MockIncomingDendrite('message contains oh snap!')
        self.instance.tourettes.neuron(object, dendrite)

        self.assertIn('yeah WHAT?? Oh yes he DID', dendrite.chats)

    def test_tourettes_is_boom(self):
        dendrite = MockIncomingDendrite('boom')
        self.instance.tourettes.neuron(object, dendrite)

        self.assertIn(u'(\u2022_\u2022)', dendrite.chats)
        self.assertIn(u'( \u2022_\u2022)>\u2310 \u25A1-\u25A1', dendrite.chats)
        self.assertIn(u'(\u2310 \u25A1_\u25A1)', dendrite.chats)

    def test_tourettes_only_match_boom_full_word(self):
        dendrite = MockIncomingDendrite('message contains boom!')
        self.instance.tourettes.neuron(object, dendrite)

        self.assertFalse(len(dendrite.chats))

    def test_tourettes_is_sup(self):
        dendrite = MockIncomingDendrite('sup')
        self.instance.tourettes.neuron(object, dendrite)

        self.assertIn('chillin', dendrite.chats)

    def test_tourettes_only_match_sup_full_word(self):
        dendrite = MockIncomingDendrite('message contains sup!')
        self.instance.tourettes.neuron(object, dendrite)

        self.assertFalse(len(dendrite.chats))

    def test_tourettes_contains_murica(self):
        dendrite = MockIncomingDendrite('message contains murica!')
        self.instance.tourettes.neuron(object, dendrite)

        self.assertIn('fuck yeah', dendrite.chats)

    def test_tourettes_contains_hail_satan(self):
        dendrite = MockIncomingDendrite('message contains hail satan!')
        self.instance.tourettes.neuron(object, dendrite)

        self.assertIn(u'\u26E7\u26E7\u26E7\u26E7\u26E7', dendrite.chats)

    def test_tourettes_contains_race_condition(self):
        dendrite = MockIncomingDendrite('message contains race condition!')
        self.instance.tourettes.neuron(object, dendrite)

        self.assertIn('It\'s never a race condition.', dendrite.chats)

    def test_tourettes_contains_rimshot(self):
        dendrite = MockIncomingDendrite('message contains rimshot')
        self.instance.tourettes.neuron(object, dendrite)

        self.assertIn('*ting*', dendrite.chats)

    def test_tourettes_ends_with_stop(self):
        dendrite = MockIncomingDendrite('message ends with stop')
        self.instance.tourettes.neuron(object, dendrite)

        self.assertIn('Hammertime', dendrite.chats)

    def test_tourettes_contains_idk(self):
        dendrite = MockIncomingDendrite('message contains idk!')
        self.instance.tourettes.neuron(object, dendrite)

        self.assertIn((u'\u00AF\u005C\u005F\u0028\u30C4'
                       u'\u0029\u005F\u002F\u00AF'), dendrite.chats)

    def test_tourettes_frustration(self):
        dendrite = MockIncomingDendrite('stupid unittest!')
        self.instance.tourettes.neuron(object, dendrite)

        self.assertIn((u'\u0028\u256F\u00B0\u25A1\u00B0\uFF09\u256F\uFE35'
                       u'\u0020\u253B\u2501\u253B'), dendrite.chats)

    def test_tourettes_inquiries(self):
        dendrite = MockIncomingDendrite('how do i write a unittest??')
        self.instance.tourettes.neuron(object, dendrite)

        self.assertTrue(
            ('Are you sure your computer is on?' in dendrite.chats or
             'http://lmgtfy.com/?q=+write+a+unittest??' in dendrite.chats)
        )

    def test_tourettes_its_always_erikbetas_birthday(self):
        dendrite = MockIncomingDendrite(
            'oh shit its your birthday erikbeta happy birthday', 'jcb'
        )
        self.instance.tourettes.neuron(object, dendrite)

        self.assertIn(' slaps jcb', dendrite.acts)
        self.assertIn('LEAVE ERIK ALONE!', dendrite.chats)
