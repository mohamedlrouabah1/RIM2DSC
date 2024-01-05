import unittest

from models.weighting.WeightingFunction import WeightingFunction

class ConcreteWeightingFunction(WeightingFunction):
    def compute_scores(self, documents, query, indexer):
        pass
class TestWeightingFunction(unittest.TestCase):

    def test_init(self):
        weighting_function = ConcreteWeightingFunction()
        with self.assertRaises(NotImplementedError):
            weighting_function.compute_scores(None, None, None)