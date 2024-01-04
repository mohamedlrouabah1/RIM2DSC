from __future__ import annotations
from sys import stderr
from tqdm import tqdm

from models.concepts.InformationRessource import InformationRessource
from models.txt.TextIndexer import TextIndexer
from models.xml.XMLDocument import XMLDocument
from models.xml.XMLElement import XMLElement
from models.xml.XMLPreprocessor import XMLPreprocessor

class XMLIndexer(TextIndexer):

    def __init__(self, index_anchors=False):
        super().__init__()
        self.index_anchors = index_anchors

    def _index_fields(self, xml_element:XMLElement) -> None:
        self._index_text(xml_element, content=xml_element.get_text_content())
        # after indexing we don't need to keep the tokens in memory
        xml_element.content = None


        if not hasattr(xml_element, "childs"):
            return

        for _, field in xml_element.childs.items():
            self._index_fields(field)


    def index(self, xml_documents:list[XMLDocument], use_parallel_computing=False) -> None:
        for xml_doc in tqdm(xml_documents, desc=f"Indexing XML documents", file=stderr):
            self._index_fields(xml_doc.content)

        if self.index_anchors:
            self._index_anchors()


    def _index_anchors(self) -> None:
        for link in tqdm(XMLPreprocessor.anchors, desc="Indexing anchors", file=stderr):
            _, id, anchor = link
            self._index_text(InformationRessource(id, anchor))

        #XMLPreprocessor.links_node = None # maybe we will use it elsewhere
