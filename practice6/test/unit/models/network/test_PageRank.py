import unittest
from models.network.PageRank import PageRank

class TestPageRank(unittest.TestCase):

    def setUp(self):
        self.pagerank = PageRank()

    def test_init(self):
        self.assertIsInstance(self.pagerank, PageRank)

    def test_compute(self):
        self.pagerank.compute()

    def test_get_ranking(self):
        self.pagerank.get_ranking()
