from abc import ABC, abstractmethod
from models.concepts.InformationRessource import InformationRessource
from models.txt.TextIndexer import TextIndexer

class WeightingFunction(ABC):
    """
    Abstract base class for weighting functions used in information retrieval.

    Methods:
        compute_scores(documents, query, indexer) -> dict[str, float]:
        Computes scores for each document based on a given query and a text indexer.

    """

    @abstractmethod
    def compute_scores(self, documents:list[InformationRessource], query:list[str], indexer: TextIndexer) -> dict[str, float]:
        raise NotImplementedError("Should implement get_ranking()")
