import unittest
from models.xml.XMLElement import XMLElement

class TestXMLElement(unittest.TestCase):

    def setUp(self):
        # Create a sample XMLElement for testing
        attributes = {'attr1': 'value1', 'attr2': 'value2'}
        childs = {'child1': XMLElement('child1', '/root/child1', {}, ['Child Text 1'], {}),
                  'child2': XMLElement('child2', '/root/child2', {}, ['Child Text 2'], {})}
        self.xml_element = XMLElement('doc_id:/root', '/root', attributes, ['Text Content'], childs)

    def test_init(self):
        self.assertIsInstance(self.xml_element, XMLElement)

    def test_str(self):
        str_representation = str(self.xml_element)
        self.assertTrue('ID: doc_id:/root' in str_representation)
        self.assertTrue('Attributes: {' in str_representation)
        self.assertTrue('Number of childs: 2' in str_representation)
        self.assertTrue('Content: [' in str_representation)

    def test_len(self):
        length = len(self.xml_element)
        self.assertEqual(length, 3)  # 1 (Text Content) + 2 (Child Text 1, Child Text 2)

    def test_get_doc_id(self):
        doc_id = self.xml_element.get_doc_id()
        self.assertEqual(doc_id, 'doc_id')

    def test_get_xpath(self):
        xpath = self.xml_element.get_xpath()
        self.assertEqual(xpath, '/root')

    def test_next_child(self):
        child_generator = self.xml_element.next_child()
        next_child = next(child_generator, None)
        self.assertIsNotNone(next_child)
        self.assertIsInstance(next_child, XMLElement)

    def test_get_text_content(self):
        text_content = self.xml_element.get_text_content()
        self.assertIn('Text Content', text_content)
        self.assertIn('Child Text 1', text_content)
        self.assertIn('Child Text 2', text_content)

    def test_get_xml_element_list(self):
        xml_element_list = self.xml_element.get_xml_element_list()
        self.assertIsInstance(xml_element_list, list)
        self.assertIn(self.xml_element, xml_element_list)
        for child in self.xml_element.childs.values():
            self.assertIn(child, xml_element_list)

if __name__ == "__main__":
    unittest.main()
