import xml.dom.minidom as minidom
import os
from sys import stderr
from string import punctuation

from utilities.config import STOPWORDS_DIR, START_TAG
from models.txt.TextPreprocessor import TextPreprocessor
from models.xml.XMLDocument import XMLDocument
from models.xml.XMLElement import XMLElement

class XMLPreprocessor(TextPreprocessor):

    def __init__(self, exclude_stopwords=True, exclude_digits=True, tokenizer="nltk", lemmer=None, stemmer="None", collection_pattern=None):
        super().__init__(exclude_stopwords, exclude_digits, tokenizer, lemmer, stemmer)
        print("XMLIndexer constructor ...")
        print(f"args: exclude_stopwords={exclude_stopwords}, exclude_digits={exclude_digits}, tokenizer={tokenizer}, lemmer={lemmer}, stemmer={stemmer}")
        
    
    def _update_xpath(self, xpath:str, tag_name:str, existing_xpath:dict) -> str:
        i = 1
        while f'{xpath}/{tag_name}[{i}]' in existing_xpath:
            i += 1
            
        return f'{xpath}/{tag_name}[{i}]'
    
    def _fetch_articles(self, dir_collection:str) -> list[tuple[str, minidom.Document]]:
        xml_files = [f for f in os.listdir(dir_collection) if f.lower().endswith('.xml')]
        articles = []
        for xml_file in xml_files:
            file_path = os.path.join(dir_collection, xml_file)
            id = xml_file.split('.')[0]
            dom = minidom.parse(file_path)
            articles += [(id, dom)]
        return articles
    
    def load(self, path) -> list[tuple[str, minidom.Document]]:
        return self._fetch_articles(path)

    def _browse(self, node:minidom.Node, xpath:str, id:str) -> XMLElement:
        childs:dict('xpath','XMLElement') = {}
        text_content:list[str] = []

        for child_node in node.childNodes:
           if child_node.nodeType == minidom.Node.ELEMENT_NODE:
               child_xpath = self._update_xpath(xpath, child_node.tagName, childs)
               child_xml_element = self._browse(child_node, child_xpath, id)
               childs[child_xpath] = child_xml_element
           
           elif child_node.nodeType == minidom.Node.TEXT_NODE:   
               if (raw_text := child_node.nodeValue.strip()):
                    text_content += self._text_preprocessing(raw_text)
                        
        return XMLElement(id, xpath, node.attributes, text_content, childs)

    def pre_process(self, raw_collection:list[tuple[str, minidom.Document]], use_parallel_computing=False) -> list[XMLDocument]:
        """
        Preprocess the raw collection and return a list of TextDocument objects.
        """
        xml_documents = []
        for doc_id, dom in raw_collection:
            start_node = dom.getElementsByTagName(START_TAG)[0]
            xpath = self._update_xpath("", start_node.tagName, {})
            xml_elements = self._browse(
                start_node, xpath, doc_id
                )
            xml_documents += [XMLDocument(doc_id, xml_elements)]

        return xml_documents