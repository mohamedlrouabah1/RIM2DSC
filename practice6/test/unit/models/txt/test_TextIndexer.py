import unittest
from models.txt.TextIndexer import TextIndexer
from models.txt.TextDocument import TextDocument

class TestTextIndexer(unittest.TestCase):

    def setUp(self):
        self.text_indexer = TextIndexer()

    def test_init(self):
        self.assertIsInstance(self.text_indexer, TextIndexer)

    def test_indexing(self):
        doc_id, doc_content = 1, ["apple", "banana", "apple", "orange"]
        text_document = TextDocument(doc_id, doc_content)

        self.text_indexer.index([text_document])

        # Check if the posting lists are created as expected
        vocabulary = self.text_indexer.get_vocabulary()
        self.assertIn("apple", vocabulary)
        self.assertIn("banana", vocabulary)
        self.assertIn("orange", vocabulary)

        df_apple = self.text_indexer.get_df("apple")
        df_banana = self.text_indexer.get_df("banana")
        df_orange = self.text_indexer.get_df("orange")

        self.assertEqual(df_apple, 1)  # One document contains "apple"
        self.assertEqual(df_banana, 1)  # One document contains "banana"
        self.assertEqual(df_orange, 1)  # One document contains "orange"

        tf_apple = self.text_indexer.get_tf("apple", doc_id)
        tf_banana = self.text_indexer.get_tf("banana", doc_id)
        tf_orange = self.text_indexer.get_tf("orange", doc_id)

        self.assertEqual(tf_apple, 2)  # "apple" appears twice in the document
        self.assertEqual(tf_banana, 1)  # "banana" appears once in the document
        self.assertEqual(tf_orange, 1)  # "orange" appears once in the document

if __name__ == "__main__":
    unittest.main()
