from models.concepts.InformationRessource import InformationRessource
from models.xml.XMLElement import XMLElement

class XMLDocument(InformationRessource):
    def __init__(self, id:int, dom:XMLElement):
        super().__init__(id, dom)
