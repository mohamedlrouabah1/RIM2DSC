from models.concepts.CollectionOfRessources import CollectionOfRessources
from models.xml.XMLDocument import XMLDocument
from types import Any

class XMLCollection(CollectionOfRessources):

    def __init__(self, id:int, documents:dict(XMLDocument)):
        super().__init__(id, documents)

    def load(self) -> Any:
        raise NotImplementedError("Should implement load()")

    def preprocess(self) -> None:
        raise NotImplementedError("Should implement preprocessing()")

    def index(self) -> None:
        raise NotImplementedError("Should implement indexing()")
    
    def compute_RSV(self, query:str) -> dict(int):
        raise NotImplementedError("Should implement query()")
    
    def compute_stats(self) -> dict(int):
        raise NotImplementedError("Should implement compute_stats()")