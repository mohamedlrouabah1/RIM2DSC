from abc import ABC, abstractmethod
from types import Any
from models.Timer import Timer
from models.concepts.InformationRessource import InformationRessource
from models.weighting.WeightingFunction import WeightingFunction

class CollectionOfRessources(ABC):

    def __init__(self, path:str, ressourcesCollection:dict(InformationRessource), use_parallel_computing=False):
        self.id = id
        self.path = path
        self.collection = ressourcesCollection
        self.use_parallel_computing = use_parallel_computing
        self.Timer = Timer()
        self.information_retriever = None

    def __len__(self):
        return len(self.collection)

    def set_ranking_function(self, ranking_function:WeightingFunction) -> None:
        self.information_retriever = ranking_function

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