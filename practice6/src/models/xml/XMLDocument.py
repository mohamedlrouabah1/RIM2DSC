from models.concepts.InformationRessource import InformationRessource
from models.xml.XMLElement import XMLElement

class XMLDocument(InformationRessource):
    """ 
    granularity set to ["element"] in order to browse all tags
    """
    granularity = ["element"] # exemple
    granularity_weights = {"element" : 1} # exemple

    @classmethod
    def set_granularity(cls, granularity:str):
        cls.granularity = granularity

    def __init__(self, id:int, dom:XMLElement):
        super().__init__(id, dom)

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