from abc import ABC, abstractmethod
from types import Any
from models.concepts.InformationRessource import InformationRessource

class CollectionOfRessources(ABC):

    def __init__(self, path:str, ressourcesCollection:dict(InformationRessource)):
        self.id = id
        self.path = path
        self.collection = ressourcesCollection

    def __len__(self):
        return len(self.collection)

    @abstractmethod
    def load(self) -> Any:
        raise NotImplementedError("Should implement load()")

    @abstractmethod
    def preprocess(self) -> None:
        raise NotImplementedError("Should implement preprocessing()")

    @abstractmethod
    def index(self) -> None:
        raise NotImplementedError("Should implement indexing()")
    
    @abstractmethod
    def compute_RSV(self, query:str) -> dict(int):
        raise NotImplementedError("Should implement query()")
    
    @abstractmethod
    def compute_stats(self) -> dict(int):
        raise NotImplementedError("Should implement compute_stats()")