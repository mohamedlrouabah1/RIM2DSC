from models.concepts.InformationRessource import InformationRessource
from models.xml.XMLElement import XMLElement

class XMLDocument(InformationRessource):

    @classmethod
    def create_xml_element(cls, xml_dict:dict) -> list(XMLElement):
        raise NotImplementedError("TODO!!")

    def __init__(self, id:int, preprocess_xml:dict):
        super().__init__(id, None)
        # to do create the XMLElement from the preprocess_xml dictionnary
        self.content:XMLElement = XMLDocument.create_xml_element(preprocess_xml)
