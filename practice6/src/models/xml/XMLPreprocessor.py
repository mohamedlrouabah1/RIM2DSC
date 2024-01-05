from __future__ import annotations
import os
from xml.dom import minidom
from tqdm import tqdm


from utilities.config import START_TAG
from models.txt.TextPreprocessor import TextPreprocessor
from models.xml.XMLDocument import XMLDocument
from models.xml.XMLElement import XMLElement

class XMLPreprocessor(TextPreprocessor):

    anchors:list[tuple(str, str, list[str])] = []

    def __init__(self, exclude_stopwords=True, exclude_digits=True, tokenizer="nltk", lemmer=None, stemmer="None", collection_pattern=None):
        super().__init__(exclude_stopwords, exclude_digits, tokenizer, lemmer, stemmer)
        self.collection_pattern = collection_pattern
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
        for xml_file in tqdm(xml_files, desc="loading xml files ..."):
            file_path = os.path.join(dir_collection, xml_file)
            doc_id = xml_file.split('.')[0]
            dom = minidom.parse(file_path)
            articles += [(doc_id, dom)]

        return articles

    def load(self, path) -> list[tuple[str, minidom.Document]]:
        return self._fetch_articles(path)

    def _extract_text(self, node, doc_id):
        """
        Extract recursively the text content of all children tags of a tag.
        Args:
        - node: a minidom.Node object.

        Returns:
        -the extracted text content as a raw string.
        """
        text = ""

        if node.nodeType == minidom.Node.ELEMENT_NODE:
            for child_node in node.childNodes:
                text += self._extract_text(child_node, doc_id)

                if  child_node.nodeType == minidom.Node.ELEMENT_NODE and child_node.tagName == "link":
                    # we extract the text content from the tree
                    raw_str = self._extract_text(child_node, doc_id)
                    if (raw_str := raw_str.strip()):
                        anchor_tokens = self._text_preprocessing(raw_str)
                    else:
                        print("anchor_tokens empty")
                        anchor_tokens = []

                    referred_doc_id = child_node.getAttribute('xlink:href').split('/')[-1].split('.')[0]
                    referred_doc_id  =  f'{referred_doc_id}:/article[1]'
                    XMLPreprocessor.anchors += [(doc_id, referred_doc_id, anchor_tokens)]

        elif node.nodeType == minidom.Node.TEXT_NODE:
            text += node.nodeValue.strip()

        return text

    def _browse(self, node:minidom.Node, xpath:str, doc_id:str) -> XMLElement:
        childs:dict('xpath','XMLElement') = {}
        text_content:list[str] = []

        for child_node in node.childNodes:
           if child_node.nodeType == minidom.Node.ELEMENT_NODE:
                # Does it belong to the granularity list
                if ("element" in XMLDocument.granularity) or (child_node.tagName in XMLDocument.granularity):
                    child_xpath = self._update_xpath(xpath, child_node.tagName, childs)
                    child_xml_element = self._browse(child_node, child_xpath, doc_id)
                    childs[child_xpath] = child_xml_element

                else:
                    # we extract the text content from the tree
                    raw_str = self._extract_text(child_node, doc_id)
                    if (raw_str := raw_str.strip()):
                        text_content += self._text_preprocessing(raw_str)

                if child_node.tagName == "link":
                    # we extract the text content from the tree
                    raw_str = self._extract_text(child_node, doc_id)
                    if (raw_str := raw_str.strip()):
                        anchor_tokens = self._text_preprocessing(raw_str)
                        text_content += anchor_tokens
                    else:
                        print("anchor_tokens empty")
                        anchor_tokens = []

                    referred_doc_id = child_node.getAttribute('xlink:href').split('/')[-1].split('.')[0]
                    referred_doc_id  =  f'{referred_doc_id}:/article[1]'
                    XMLPreprocessor.anchors += [(doc_id, referred_doc_id, anchor_tokens)]

           elif child_node.nodeType == minidom.Node.TEXT_NODE:
               if (raw_text := child_node.nodeValue.strip()):
                    text_content += self._text_preprocessing(raw_text)

        return XMLElement(doc_id, xpath, node.attributes, text_content, childs)

    def pre_process(self, raw_collection:list[tuple[str, minidom.Document]], use_parallel_computing=False) -> list[XMLDocument]:
        """
        Preprocess the raw collection and return a list of TextDocument objects.
        """
        xml_documents = []
        for doc_id, dom in tqdm(raw_collection, desc="preprocessing xml documents ..."):
            start_node = dom.getElementsByTagName(START_TAG)[0]
            xpath = self._update_xpath("", start_node.tagName, {})
            xml_elements = self._browse(
                start_node, xpath, doc_id
                )
            xml_documents += [XMLDocument(doc_id, xml_elements)]

        return xml_documents
