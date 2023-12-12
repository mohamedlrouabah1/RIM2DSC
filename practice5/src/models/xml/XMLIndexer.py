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
        self._index_text(xml_element, content=xml_element.get_text_content())
        
        if not hasattr(xml_element, "childs"):
            return
        
        for _, field in xml_element.childs.items():
            self._index_fields(field)


    def index(self, xml_documents:list[XMLDocument], use_parallel_computing=False) -> None:
        for xml_doc in tqdm(xml_documents, desc=f"Indexing XML documents", file=stderr):
            self._index_fields(xml_doc.content)
