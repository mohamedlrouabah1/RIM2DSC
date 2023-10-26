from abc import ABC, abstractmethod

class WeightingFunction(ABC):

    @abstractmethod
    def compute_score(self, **kargs):
        raise NotImplementedError("Should implement get_ranking()")