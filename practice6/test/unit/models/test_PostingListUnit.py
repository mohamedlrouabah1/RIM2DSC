import unittest
from models.PostingListUnit import PostingListUnit

class TestPostingListUnit(unittest.TestCase):

    def test_init(self):
        """Test the initialization of PostingListUnit"""
        document_id, frequency = 1, 2.5
        posting_unit = PostingListUnit(document_id, frequency)

        self.assertEqual(posting_unit.document_id, document_id)
        self.assertEqual(posting_unit.frequency, frequency)

    def test_str(self):
        """ Test the __str__ method of PostingListUnit"""
        document_id = 1
        frequency = 2.5
        posting_unit = PostingListUnit(document_id, frequency)

        # Verify the string representation
        expected_str = f"Document ID: {document_id} - Frequency: {frequency}"
        self.assertEqual(str(posting_unit), expected_str)

if __name__ == "__main__":
    unittest.main()
