from functools import lru_cache
from math import log10

from models.concepts.InformationRessource import InformationRessource
from models.txt.TextIndexer import TextIndexer
from models.weighting.WeightingFunction import WeightingFunction


class SMART_lnu(WeightingFunction):
    """
    Implementation of the SMART_lnu weighting function.

    Methods:
        compute_scores(documents, query, indexer) -> dict[str, float]:
        Computes SMART_lnu scores for each document based on a given
        query and a text indexer.

    """

    def __init__(self, N, slope):
        """
        Initialize the SMART_lnu weighting function.

        Params:
        -------
        N: int
            Number of documents in the collection.
        slope: float
            Slope parameter for the SMART_lnu function.

        """
        self.N = N
        self.slope = slope

    @lru_cache(maxsize=1024)
    def _compute_weight(self, tf:float, dl_on_avdl:float, nt_d:float, den_part1:float) -> float:
        """
        Compute the SMART_lnu weight for a term in a document.

        Params:
        -------
        tf: float
            Term frequency in the document.
        dl_on_avdl: float
            Ratio of document length to average document length.
        nt_d: float
            Number of distinct terms in the document.
        den_part1: float
            Denominator part of the SMART_lnu function.

        Returns:
        --------
        float: SMART_lnu weight for the term in the document.

        """
        num = 1 + log10(tf) if tf > 0 else 0

        if dl_on_avdl > 0:
            tmp = log10(dl_on_avdl) # log10(0.1) = -1
            if tmp > 0:
                num /= (1 + log10(dl_on_avdl))
            else:
                num = 0
        else:
            num = 0

        den = den_part1 + self.slope * nt_d

        return num / den

    def compute_scores(self, documents:list[InformationRessource], query:list[str], indexer:TextIndexer) -> dict[str, float]:
        """
        Computes SMART_lnu scores for each document based on a given
        query and a text indexer.

        Params:
        -------
        documents: list of InformationRessource
            List of documents to compute scores for.
        query: list of str
            Query terms.
        indexer: TextIndexer
            Text indexer containing document statistics.

        Returns:
        --------
        dict[str, float]: Dictionary of scores for each document,
                          where keys are document ids.

        """
        scores = {}
        avdl = indexer.avdl
        pivot = indexer.average_nb_distinct_terms
        den_part1 = (1 - self.slope) * pivot
        for doc in documents:
            score = 0
            dl_on_avdl = len(doc) / avdl
            nt_d = indexer.nb_distinct_terms[doc.id.split(':')[0]]
            for term in query:
                tf = indexer.get_tf(term, doc.id)
                score += self._compute_weight(tf, dl_on_avdl, nt_d, den_part1)
            scores[doc.id] = score

        return scores
