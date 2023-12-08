from sys import stderr
from tqdm import tqdm
from models.txt.TextIndexer import TextIndexer
from models.xml.XMLDocument import XMLDocument

class XMLIndexer(TextIndexer):
    
    def __init__(self):
        super().__init__()

    def _index_fields(self, xml_element:XMLDocument) -> None:
        self._index_text(xml_element.content)
        for field in xml_element.fields:
            self._index_text(field)

    def index(self, xml_documents:list[XMLDocument], use_parallel_computing=False) -> None:
        for xml_doc in tqdm(xml_documents, desc="Indexing XML documents", file=stderr):
            self._index_fields(xml_doc.content)