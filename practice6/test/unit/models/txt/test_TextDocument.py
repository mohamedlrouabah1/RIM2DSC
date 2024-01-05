import unittest

from models.txt.TextDocument import TextDocument

class TestTextDocument(unittest.TestCase):

    def test_init(self):
        text_document = TextDocument('doc_id', 'doc_path', 'doc_content')
        self.assertIsInstance(text_document, TextDocument)
