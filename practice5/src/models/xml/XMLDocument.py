from models.concepts.InformationRessource import InformationRessource
from models.xml.XMLElement import XMLElement

class XMLDocument(InformationRessource):
    def __init__(self, id:int, dom:XMLElement):
        super().__init__(id, dom)

    def __len__(self) -> int:
        return len(self.content)
    
    def get_text_content(self) -> list[str]:
        return self.content.get_text_content()
    
    def get_xml_element_list(self) -> list[XMLElement]:
        return self.content.get_xml_element_list()
    
    def compute_avtl(self) -> float:
        print("XMLDocument compute_avtl ...")
        tokens = self.get_text_content()
        print(f"XMLDocument compute_avtl: {self.id} nb tokens: {len(tokens)}")
        num = sum(len(t) for t in tokens)
        return num / len(tokens)