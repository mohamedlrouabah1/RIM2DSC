import unittest
from models.PostingList import PostingList
from models.PostingListUnit import PostingListUnit

class TestPostingList(unittest.TestCase):

    def test_init(self):
        """ Test the initialization of PostingList"""
        term = "test_term"
        posting_list = PostingList(term)

        # Verify that attributes are set correctly
        self.assertEqual(posting_list.term, term)
        self.assertEqual(len(posting_list), 0)
        self.assertEqual(posting_list.document_frequency, 0)
        self.assertEqual(posting_list.total_frequency, 0)
        self.assertEqual(posting_list.doc_ids, set())
        self.assertEqual(posting_list.postings, {})

    def test_add_posting(self):
        """  Test the add_posting method of PostingList"""
        term = "test_term"
        posting_list = PostingList(term)

        # Create PostingListUnit
        document_id = "doc1"
        frequency = 2.5
        posting_unit = PostingListUnit(document_id, frequency)

        # Add posting to the posting list
        posting_list.add_posting(posting_unit)

        # Verify that attributes are updated correctly
        self.assertEqual(len(posting_list), 1)
        self.assertEqual(posting_list.document_frequency, 1)
        self.assertEqual(posting_list.total_frequency, frequency)
        self.assertEqual(posting_list.doc_ids, {document_id})
        self.assertEqual(posting_list.postings[document_id], posting_unit)

    def test_get_tfd(self):
        """ Test the get_tfd method of PostingList"""
        term = "test_term"
        posting_list = PostingList(term)

        # Create PostingListUnit
        document_id = "doc1"
        frequency = 2.5
        posting_unit = PostingListUnit(document_id, frequency)

        # Add posting to the posting list
        posting_list.add_posting(posting_unit)

        # Test get_tfd for an existing document_id
        tfd = posting_list.get_tfd(document_id)
        self.assertEqual(tfd, frequency)

        # Test get_tfd for a non-existing document_id
        non_existing_doc_id = "non_existing_doc"
        tfd_non_existing = posting_list.get_tfd(non_existing_doc_id)
        self.assertEqual(tfd_non_existing, 0)

if __name__ == "__main__":
    unittest.main()
