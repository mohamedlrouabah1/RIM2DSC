from __future__ import annotations
from sys import stderr
from tqdm import tqdm

from models.concepts.InformationRessource import InformationRessource
from models.txt.TextIndexer import TextIndexer
from models.xml.XMLDocument import XMLDocument
from models.xml.XMLElement import XMLElement
from models.xml.XMLPreprocessor import XMLPreprocessor

class XMLIndexer(TextIndexer):

    index_anchors = False

    def _index_fields(self, xml_element:XMLElement) -> None:
        self._index_text(xml_element, content=xml_element.get_text_content())

        if not hasattr(xml_element, "childs"):
            return

        for _, field in xml_element.childs.items():
            self._index_fields(field)


    def index(self, docs:list[XMLDocument], use_parallel_computing=False) -> None:
        for xml_doc in tqdm(docs, desc='Indexing XML documents', file=stderr):
            self._index_fields(xml_doc.content)

        if XMLIndexer.index_anchors:
            self._index_anchors()


    def _index_anchors(self) -> None:
        for link in tqdm(XMLPreprocessor.anchors, desc="Indexing anchors", file=stderr):
            _, reffered_doc_id, anchor = link
            if anchor:
                self._index_text(InformationRessource(reffered_doc_id, anchor))

        #XMLPreprocessor.links_node = None # maybe we will use it elsewhere
