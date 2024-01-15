from __future__ import annotations

from models.concepts.InformationRessource import InformationRessource
from models.xml.XMLElement import XMLElement

class XMLDocument(InformationRessource):
    """
    Implementation of the XMLDocument class, representing an XML document.

    Class Attributes:
    -----------------
    - granularity: list of str
        Granularity set to ["element"] in order to browse all tags.
    - granularity_weights: dict
        Granularity weights for different elements in the document.

    Class Methods:
    --------------
    - set_granularity(cls, granularity: str) -> None:
        Set the granularity of the XMLDocument.

    Methods:
    --------
    - __init__(self, doc_id: int, dom: XMLElement) -> None:
        Initialize an XMLDocument instance with a document ID and an XMLElement.
    - __len__(self) -> int:
        Return the length of the XMLDocument.
    - __str__(self) -> str:
        Return a string representation of the XMLDocument.
    - get_text_content(self) -> list[str]:
        Get the text content of the XMLDocument.
    - get_xml_element_list(self) -> list[XMLElement]:
        Get a list of XML elements in the XMLDocument.
    - compute_avtl(self) -> float:
        Compute the average token length in the XMLDocument.
    - del_tokens_list(self) -> None:
        Delete the tokens list in the content.

    """
    granularity = ["element"] # exemple
    granularity_weights = {"element" : 1} # exemple

    @classmethod
    def set_granularity(cls, granularity:list[str]):
        cls.granularity = granularity

    def __init__(self, doc_id:int, dom:XMLElement):
        """
        Initialize an XMLDocument instance with a document ID and an XMLElement.

        Params:
        -------
        - doc_id: int
            Document ID.
        - dom: XMLElement
            Root XMLElement representing the XML document.
        """
        super().__init__(doc_id, dom)

    def __len__(self) -> int:
        return len(self.content)

    def __str__(self) -> str:
        return f"XMLDocument {self.id} :\n {self.content.__str__()}"

    def get_text_content(self) -> list[str]:
        return self.content.get_text_content()

    def get_xml_element_list(self) -> list[XMLElement]:
        return self.content.get_xml_element_list()

    def compute_avtl(self) -> float:
        tokens = self.get_text_content()
        num = sum(len(t) for t in tokens)
        return num / len(tokens)

    def del_tokens_list(self) -> None:
        self.content._del_tokens_list()
