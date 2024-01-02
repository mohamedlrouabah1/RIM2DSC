from models.concepts.InformationRessource import InformationRessource
class XMLElement(InformationRessource):

    def __init__(self, id:str, xpath:str, attributes:dict, text_content:list[str], childs:dict[str,'XMLElement']):
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