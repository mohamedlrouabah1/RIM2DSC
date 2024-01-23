from __future__ import annotations
from sys import stderr
from tqdm import tqdm

from models.concepts.InformationRessource import InformationRessource
from models.txt.TextIndexer import TextIndexer
from models.xml.XMLDocument import XMLDocument
from models.xml.XMLElement import XMLElement
from models.xml.XMLPreprocessor import XMLPreprocessor

class XMLIndexer(TextIndexer):
    """
    Indexer for XML documents, responsible for extracting and indexing relevant information
    from XML elements.

    Class Attributes:
    -----------------
    - index_anchors: bool
        Flag indicating whether to index anchors.

    Methods:
    --------
    - _index_fields(self, xml_element: XMLElement) -> None:
        Recursively index the text content of an XML element and its child elements.
    - index(self, docs: list[XMLDocument], use_parallel_computing: bool = False) -> None:
        Index the XML documents, extracting and indexing relevant information.
    - _index_anchors(self) -> None:
        Index the anchors found during XML preprocessing.

    """

    index_anchors = False

    def _index_fields(self, xml_element:XMLElement) -> None:
        """
        Recursively index the text content of an XML element and its child elements.

        Params:
        -------
        - xml_element: XMLElement
            The XML element to index.
        """
        self._index_text(xml_element, content=xml_element.get_text_content())

        if not hasattr(xml_element, "childs"):
            return

        for _, field in xml_element.childs.items():
            self._index_fields(field)


    def index(self, docs:list[XMLDocument], use_parallel_computing=False) -> None:
        """
        Index the XML documents, extracting and indexing relevant information.

        Params:
        -------
        - docs: list[XMLDocument]
            List of XML documents to index.
        - use_parallel_computing: bool, optional
            Flag indicating whether to use parallel computing.
        """
        for xml_doc in tqdm(docs, desc='Indexing XML documents', file=stderr):
            self._index_fields(xml_doc.content)

        if XMLIndexer.index_anchors:
            self._index_anchors()


    def _index_anchors(self) -> None:
        """Index the anchors found during XML preprocessing."""
        for link in tqdm(XMLPreprocessor.anchors, desc="Indexing anchors", file=stderr):
            _, reffered_doc_id, anchor = link
            if anchor:
                id, xpath = reffered_doc_id.split(':')
                xml_elemnt = XMLElement(id, xpath, {}, anchor, {})
                self._index_text(xml_elemnt)

        #XMLPreprocessor.links_node = None # maybe we will use it elsewhere like in page rank algo or NSA algo
