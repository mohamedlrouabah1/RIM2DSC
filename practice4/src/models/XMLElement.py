from typing import TypeVar

T = TypeVar('T', bound='XMLElement')

class XMLElement():

    @classmethod
    def parse_inner_content(cls:type[T], inner_content:str) -> T:
        """
        Parse the inner content of a XML element
        """
        # TODO
        pass

    def __init__(self, tag, attributes, children):
        self.tag = tag
        self.attributes = attributes
        self.children = children

    def __str__(self):
        return f'<{self.tag} {self.attributes}>\n{self.children}\n</{self.tag}>'