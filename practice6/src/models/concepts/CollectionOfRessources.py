from __future__ import annotations
from abc import ABC, abstractmethod

from models.Timer import Timer
from models.concepts.InformationRessource import InformationRessource
from models.weighting.WeightingFunction import WeightingFunction

class CollectionOfRessources(ABC):
    """
    Abstract class representing a collection of information resources.

    Attributes:
        id (int): The identifier of the collection.
        path (str): The path to the collection of resources.
        collection (dict[str, InformationRessource]): A dictionary of information resources.
        use_parallel_computing (bool): Indicates whether parallel processing is enabled.
        Timer (Timer): Timer object to measure execution time.
        information_retriever (WeightingFunction): Weighting function for resource ranking.

    Methods:
        __len__(): Returns the size of the collection.
        set_ranking_function(ranking_function: WeightingFunction) -> None: Sets the weighting function.
        load() -> 'any': Abstract method to load the collection.
        preprocess(raw_collection) -> None: Abstract method to preprocess the collection.
        index() -> None: Abstract method to index the resources.
        compute_RSV(query: str) -> dict[str, float]: Abstract method to calculate RSV values.
        compute_stats() -> None: Abstract method to calculate collection statistics.
    """

    def __init__(self, path:str, ressourcesCollection:dict[str,InformationRessource], use_parallel_computing=False):
        self.id = id
        self.path = path
        self.collection = ressourcesCollection
        self.use_parallel_computing = use_parallel_computing
        self.Timer = Timer()
        self.information_retriever:WeightingFunction = None

    def __len__(self):
        return len(self.collection)

    def set_ranking_function(self, ranking_function:WeightingFunction) -> None:
        self.information_retriever = ranking_function

    @abstractmethod
    def load(self) -> 'any':
        raise NotImplementedError("Should implement load()")

    @abstractmethod
    def preprocess(self, raw_collection) -> None:
        raise NotImplementedError("Should implement preprocessing()")

    @abstractmethod
    def index(self) -> None:
        raise NotImplementedError("Should implement indexing()")

    @abstractmethod
    def compute_RSV(self, query:str) -> dict[str, float]:
        raise NotImplementedError("Should implement query()")

    @abstractmethod
    def compute_stats(self) -> None:
        raise NotImplementedError("Should implement compute_stats()")