import unittest
from models.concepts.CollectionOfRessources import CollectionOfRessources

class TestCollectionOfRessources(unittest.TestCase):

    def setUp(self):
        self.collection_of_ressources = CollectionOfRessources(path="test_path", ressourcesCollection={}, use_parallel_computing=False)

    def test_init(self):
        self.assertIsInstance(self.collection_of_ressources, CollectionOfRessources)

    def test_abstract_methods(self):
        with self.assertRaises(NotImplementedError):
            self.collection_of_ressources.load()

        with self.assertRaises(NotImplementedError):
            self.collection_of_ressources.preprocess()

        with self.assertRaises(NotImplementedError):
            self.collection_of_ressources.index()

        with self.assertRaises(NotImplementedError):
            self.collection_of_ressources.compute_RSV("query")

        with self.assertRaises(NotImplementedError):
            self.collection_of_ressources.compute_stats()

if __name__ == "__main__":
    unittest.main()
