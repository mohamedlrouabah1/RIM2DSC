import unittest
from models.xml.XMLDocument import XMLDocument
from models.xml.XMLElement import XMLElement

class TestXMLDocument(unittest.TestCase):

    def setUp(self):
        sample_element = XMLElement("sample_id", "sample_xpath", {}, ["sample_text"], {})
        self.xml_document = XMLDocument(1, sample_element)

    def test_init(self):
        self.assertIsInstance(self.xml_document, XMLDocument)

if __name__ == "__main__":
    unittest.main()
