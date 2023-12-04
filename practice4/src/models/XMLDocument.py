from concepts.InformationRessource import InformationRessource

class XMLDocument(InformationRessource):
    
    def __init__(self, id:int, raw_content:str, xpath:str):
        super().__init__(id, None)
        self.xpath = xpath
        # TODO : parse raw_content to extract the content of the document