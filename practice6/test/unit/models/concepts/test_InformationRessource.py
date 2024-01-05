import unittest
from models.concepts.InformationRessource import InformationRessource

class TestInformationRessource(unittest.TestCase):

    def setUp(self):
        self.information_ressource = InformationRessource(id=1, content="Test content")

    def test_init(self):
        self.assertIsInstance(self.information_ressource, InformationRessource)

    def test_len(self):
        self.assertEqual(len(self.information_ressource), len("Test content"))

    def test_str(self):
        self.assertEqual(str(self.information_ressource), "Document 1 {} pieces of information.".format(len("Test content")))

    def test_repr(self):
        repr_string = self.information_ressource.__repr__()
        self.assertIsInstance(repr_string, str)

    def test_get_id(self):
        self.assertEqual(self.information_ressource.get_id(), 1)

    def test_get_content(self):
        self.assertEqual(self.information_ressource.get_content(), "Test content")

if __name__ == "__main__":
    unittest.main()
