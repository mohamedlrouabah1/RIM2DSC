import unittest
from models.txt.TextCollection import TextCollection

class TestTextCollection(unittest.TestCase):

    COLL_PATH = "../../data/Practice_05_data/XML-Coll-withSem/"

    def setUp(self):
        self.text_collection = TextCollection(path=TestTextCollection.COLL_PATH)

    def test_init(self):
        self.assertIsInstance(self.text_collection, TextCollection)
        self.assertEqual(self.text_collection.path, TestTextCollection.COLL_PATH)

if __name__ == "__main__":
    unittest.main()
