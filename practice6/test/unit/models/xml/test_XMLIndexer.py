import unittest
from models.xml.XMLIndexer import XMLIndexer

class TestXMLIndexer(unittest.TestCase):

    def setUp(self):
        self.xml_indexer = XMLIndexer()

    def test_init(self):
        self.assertIsInstance(self.xml_indexer, XMLIndexer)

if __name__ == "__main__":
    unittest.main()
