import unittest
from models.txt.TextPreprocessor import TextPreprocessor

class TestTextPreprocessor(unittest.TestCase):

    def setUp(self):
        self.text_preprocessor = TextPreprocessor()

    def test_init(self):
        self.assertIsInstance(self.text_preprocessor, TextPreprocessor)

    def test_text_preprocessing(self):
        text = "This is a test document with some stopwords."
        processed_text = self.text_preprocessor._text_preprocessing(text)
        
        self.assertIsInstance(processed_text, list)
        self.assertNotIn("stopwords", processed_text)

if __name__ == "__main__":
    unittest.main()
