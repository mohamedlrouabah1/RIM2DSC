from __future__ import annotations
from models.concepts.InformationRessource import InformationRessource
class XMLElement(InformationRessource):
    """
    Implementation of the XMLElement class, representing an element in an XML document.

    Attributes:
    -----------
    - id: str
        ID of the element (combination of document ID and XPath).
    - xpath: str
        XPath of the element.
    - attributes: dict
        Attributes of the element.
    - text_content: list[str]
        Text content of the element.
    - childs: dict[str, 'XMLElement']
        Dictionary of child elements, where the key is the XPath.

    Methods:
    --------
    - __init__(self, id: str, xpath: str, attributes: dict, text_content: list[str], childs: dict[str, 'XMLElement']) -> None:
        Initialize an XMLElement instance with an ID, XPath, attributes, text content, and child elements.
    - __str__(self) -> str:
        Return a string representation of the XMLElement.
    - __len__(self) -> int:
        Return the length of the XMLElement.
    - get_doc_id(self) -> str:
        Get the document ID of the XMLElement.
    - get_xpath(self) -> str:
        Get the XPath of the XMLElement.
    - next_child(self) -> 'XMLElement':
        Generator to iterate over child elements.
    - get_text_content(self) -> list[str]:
        Get the text content of the XMLElement and its child elements.
    - get_xml_element_list(self) -> list['XMLElement']:
        Get a list of XML elements, including the current element and its child elements.
    - _del_tokens_list(self) -> None:
        Delete the tokens list in the content to free memory RAM.

    """

    def __init__(self, id:str, xpath:str, attributes:dict, text_content:list[str], childs:dict[str,'XMLElement']):
        """
        Initialize an XMLElement instance with an ID, XPath, attributes, text content, and child elements.

        Params:
        -------
        - id: str
            ID of the element (combination of document ID and XPath).
        - xpath: str
            XPath of the element.
        - attributes: dict
            Attributes of the element.
        - text_content: list[str]
            Text content of the element.
        - childs: dict[str, 'XMLElement']
            Dictionary of child elements, where the key is the XPath.
        """
        super().__init__(f'{id}:{xpath}', text_content)
        self.attributes = attributes
        self.childs = childs
        self.len = len(self.content) + sum(len(child) for child in self.childs)

    def __str__(self) -> str:
        s = f"""
        {'+'*50}\n
        ID: {self.id}\n
        Attributes: {self.attributes}\n
        Number of childs: {len(self.childs)}\n
        Content: {self.content}\n
        """
        for xpath, child in self.childs.items():
            s += f"Child {xpath} : {child.__str__()}\n"
        s += f"{'+'*50}\n"

        return s

    def __len__(self) -> int:
        return self.len

    def get_doc_id(self) -> str:
        return self.id.split(':')[0]

    def get_xpath(self) -> str:
        return self.id.split(':')[1]

    def next_child(self) -> 'XMLElement':
        for child in self.childs:
            yield child

    def get_text_content(self) -> list[str]:
        tokens = []
        if self.childs :
            for child in self.childs.values():
                tokens += child.get_text_content()

        tokens += self.content
        return tokens

    def get_xml_element_list(self) -> list['XMLElement']:
        elements = [self]
        if len(self.childs) > 0 :
            for child in self.childs.values():
                elements += child.get_xml_element_list()
        return elements

    def _del_tokens_list(self):
        self.content = []
        for child in self.childs.values():
            child._del_tokens_list()
