from models.concepts.InformationRessource import InformationRessource
class XMLElement(InformationRessource):

    def __init__(self, id:str, xpath:str, attributes:dict, text_content:list[str], childs:dict[str,'XMLElement']):
        super().__init__(f'{id}:{xpath}', text_content)
        self.attributes = attributes
        self.childs = childs
    
    def __len__(self) -> int:
        return len(self.content) + sum(len(child) for child in self.childs)

    def get_doc_id(self) -> str:
        return self.id.split(':')[0]

    def get_xpath(self) -> str:
        return self.id.split(':')[1]
    
    def next_child(self) -> 'XMLElement':
        for child in self.childs:
            yield child

    def get_text_content(self) -> list[str]:
        tokens = self.content
        if self.childs :
            for child in self.childs.values():
                tokens += child.get_text_content()
        return tokens
    
    def get_xml_element_list(self) -> list['XMLElement']:
        elements = [self]
        print(f"elements: {self.id}")
        if self.childs :
            for child in self.childs.values():
                elements += child.get_xml_element_list()
        return elements