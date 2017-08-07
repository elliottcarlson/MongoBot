import unittest

from MongoBot.synapses import Neurons, Cerebellum, Synapse, Receptor


class TestSynapses(unittest.TestCase):

    def setUp(self):

        @Cerebellum
        class TestClass(object):

            @Receptor('SynapseUnitTest')
            def test_receptor(self):
                pass

            @Synapse('SynapseUnitTest')
            def test_synapse(self):
                pass

        self.test_class = TestClass()

    def test_registers_receptor(self):

        self.assertIn('SynapseUnitTest', Neurons.vesicles)
        v = Neurons.vesicles.get('SynapseUnitTest')
        index = next(index for (index, d) in enumerate(v) if 'testclass' in d)
        func = v[index].get('testclass')
        self.assertEquals(func.__name__, 'test_receptor')

    def test_calls_receptor(self):

        with self.assertRaises(TypeError) as context:
            self.test_class.test_synapse()

        self.assertTrue('test_receptor() takes exactly 1 argument (2 given)' in context.exception)
