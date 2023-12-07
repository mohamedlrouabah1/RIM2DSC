from models.concepts.InformationRessource import InformationRessource
class XMLElement(InformationRessource):

    def __init__(self, id:str, xpath:str, attributes:dict, text_content:str, childs:dict('xpath','XMLElement')):
        super().__init__(f'{id}:{xpath}', text_content)
        self.attributes = attributes
        self.childs = childs

    def get_doc_id(self) -> str:
        return self.id.split(':')[0]

    def get_xpath(self) -> str:
        return self.id.split(':')[1]
    
    def next_child(self) -> 'XMLElement':
        for child in self.childs:
            yield child