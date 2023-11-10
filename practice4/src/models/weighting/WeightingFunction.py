from abc import ABC, abstractmethod

class WeightingFunction(ABC):

    @abstractmethod
    def compute_scores(self, documents, query, indexer):
        raise NotImplementedError("Should implement get_ranking()")