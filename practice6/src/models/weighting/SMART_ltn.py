from functools import lru_cache
from math import log10

from models.concepts.InformationRessource import InformationRessource
from models.txt.TextIndexer import TextIndexer
from models.weighting.WeightingFunction import WeightingFunction

class SMART_ltn(WeightingFunction):
    """
    Implementation of the SMART_ltn weighting function.

    Methods:
        __init__(N)
        Initializes the SMART_ltn weighting function.

        compute_idf(df, N) -> float
        Computes the Inverse Document Frequency (IDF) part of the SMART_ltn weight.

        compute_tf_part(tf) -> float
        Computes the Term Frequency (TF) part of the SMART_ltn weight.

        compute_weight(tf, df) -> float
        Computes the SMART_ltn weight for a term in a document.

        compute_scores(documents, query, indexer) -> dict[str, float]
        Computes SMART_ltn scores for each document based on a given query
        and a text indexer.
    """

    def __init__(self, N):
        """
        Initializes the SMART_ltn weighting function.

        Params:
        -------
        N: int
            Number of documents in the collection.

        """
        super().__init__()
        self.N = N

    @lru_cache(maxsize=1024)
    def compute_idf(self, df:float, N:int) -> float:
        """
        Computes the logarithme Inverse Document Frequency (IDF) part of the SMART_ltn weight.

        Params:
        -------
        df: float
            Document frequency of the term.
        N: int
            Total number of documents in the collection.

        Returns:
        --------
        float: IDF part of the SMART_ltn weight.

        """
        return log10(N / df)

    @lru_cache(maxsize=1024)
    def compute_tf_part(self, tf:float) -> float:
        return 1 + log10(tf) if tf > 0 else 0

    @lru_cache(maxsize=1024)
    def compute_weight(self, tf:float, df:float) -> float:
        if df > 0 and self.N >= df:
            idf = self.compute_idf(df, self.N+2)
            tf_part = self.compute_tf_part(tf)
            return tf_part * idf
        return 0

    def compute_scores(self, documents:list[InformationRessource], query:list[str], indexer:TextIndexer) -> dict[str, float]:
        """
        Computes SMART_ltn scores for each document based on a given query and a text indexer.

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
        for doc in documents:
            score = 0
            for term in query:
                df = indexer.get_df(term)
                tf = indexer.get_tf(term, doc.id)
                score += self.compute_weight(tf, df)
            scores[doc.id] = score

        return scores
