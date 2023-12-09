from sys import stderr
from sys import exit
from tqdm import tqdm
from models.txt.TextIndexer import TextIndexer
from models.xml.XMLDocument import XMLDocument
from models.xml.XMLElement import XMLElement

class XMLIndexer(TextIndexer):
    
    def __init__(self):
        super().__init__()

    def _index_fields(self, xml_element:XMLElement) -> None:
        self._index_text(xml_element)
        for field in xml_element.childs.values():
            self._index_text(field)

    def index(self, xml_documents:list[XMLDocument], use_parallel_computing=False) -> None:
        for xml_doc in tqdm(xml_documents, desc="Indexing XML documents", file=stderr):
            self._index_fields(xml_doc.content)
            # Also index only the document as a text element
            self._index_text(xml_doc, content=xml_doc.content.get_text_content())