from functools import lru_cache
from sys import stderr
from math import log10, log
from models.weighting.WeightingFunction import WeightingFunction

class SMART_ltn(WeightingFunction):

    def __init__(self, N):
        """
        Param:
            N: number of documents in the collection
        """
        super().__init__()
        self.N = N

    @lru_cache(maxsize=1024)
    def compute_idf(self, df, N):
        return log10(N / df)

    @lru_cache(maxsize=1024)
    def compute_tf_part(self, tf):
        return 1 + log10(tf) if tf > 0 else 0

    @lru_cache(maxsize=1024)
    def compute_weight(self, tf, df):
        if df > 0 and self.N >= df:
            idf = self.compute_idf(df, self.N+2)
            tf_part = self.compute_tf_part(tf)
            return tf_part * idf
        return 0

    def compute_scores(self, documents, query, indexer):
        """
        Return a dictionary of scores for each document for each query.
        The keys of the dictionary are the queries ids.
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