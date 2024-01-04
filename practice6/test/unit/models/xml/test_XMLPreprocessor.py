import unittest
from unittest.mock import patch
from xml.dom.minidom import Document, parseString

from models.xml.XMLDocument import XMLDocument
from models.xml.XMLPreprocessor import XMLPreprocessor

class TestXMLPreprocessor(unittest.TestCase):

    def setUp(self):
        self.xml_preprocessor = XMLPreprocessor()

    def test_update_xpath(self):
        existing_xpath = {"xpath/tag[1]": None, "xpath/tag[2]": None}
        new_xpath = self.xml_preprocessor._update_xpath("xpath", "tag", existing_xpath)
        self.assertEqual(new_xpath, "xpath/tag[3]")

    def test_fetch_articles(self):
        with patch("os.listdir") as mock_listdir:
            mock_listdir.return_value = ["doc1.xml", "doc2.xml"]
            articles = self.xml_preprocessor._fetch_articles("path/to/xml/files")

        self.assertEqual(len(articles), 2)
        self.assertTrue(all(isinstance(item, tuple) and len(item) == 2 for item in articles))

    def test_load(self):
        with patch("os.path.join") as mock_join, \
             patch("os.listdir") as mock_listdir, \
             patch("xml.dom.minidom.parse") as mock_parse:
            mock_join.return_value = "path/to/xml/files/doc1.xml"
            mock_listdir.return_value = ["doc1.xml"]
            mock_parse.return_value = Document()
            articles = self.xml_preprocessor.load("path/to/xml/files")

        self.assertEqual(len(articles), 1)
        self.assertTrue(all(isinstance(item, tuple) and len(item) == 2 for item in articles))

    def test_extract_text(self):
        # Creating a simple XML document for testing
        xml_str = "<root><element1>Text 1</element1><element2>Text 2</element2></root>"
        dom = parseString(xml_str)
        root = dom.documentElement

        text_content = self.xml_preprocessor._extract_text(root)
        self.assertEqual(text_content, "Text 1 Text 2")

    def test_browse(self):
        # Creating a simple XML document for testing
        xml_str = "<root><element1><subelement>Text 1</subelement></element1><element2>Text 2</element2></root>"
        dom = parseString(xml_str)
        root = dom.documentElement

        xml_element = self.xml_preprocessor._browse(root, "", "doc_id")
        doc_id, xpath = xml_element.id.split(":")

        self.assertEqual(doc_id, "doc_id")
        self.assertEqual(xpath, "/article[1]")
        self.assertEqual(xml_element.content, ["Text 1", "Text 2"])
        self.assertEqual(len(xml_element.childs), 2)

    def test_pre_process(self):
        # Creating a simple XML document for testing
        xml_str = "<root><element1>Text 1</element1><element2>Text 2</element2></root>"
        dom = parseString(xml_str)
        raw_collection = [("doc_id", dom)]

        xml_documents = self.xml_preprocessor.pre_process(raw_collection)

        self.assertEqual(len(xml_documents), 1)
        self.assertTrue(all(isinstance(item, XMLDocument) for item in xml_documents))

if __name__ == "__main__":
    unittest.main()
