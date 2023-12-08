from models.concepts.InformationRessource import InformationRessource
from models.xml.XMLElement import XMLElement

class XMLDocument(InformationRessource):

    @classmethod
    def create_xml_elements(cls, xml_dict:dict) -> list(XMLElement):
        raise NotImplementedError("TODO!!")

    def __init__(self, id:int, dom:XMLElement):
        super().__init__(id, dom)
