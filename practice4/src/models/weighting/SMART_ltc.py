from functools import lru_cache
from math import log10, sqrt
from models.weighting.SMART_ltn import SMART_ltn
from models.weighting.WeightingFunction import WeightingFunction

class SMART_ltc(WeightingFunction):

    def __init__(self, N, **kargs):
        if  kargs['smart_ltn']is not None:
            self.smart_ltn = kargs['smart_ltn']
        else:
            self.smart_ltn = SMART_ltn(N)    

    def compute_scores(self, documents, query, indexer):
        """
        Return a dictionary of scores for each document for each query.
        The keys of the dictionary are the queries ids.
        """        
        scores = {}
        num = den = 0
        # Compute ltn for each document
        for doc in documents:
            for term in query:
                df = indexer.get_df(term)
                tf = indexer.get_tf(term, doc.id)

                w_t_d = self.smart_ltn.compute_weight(tf, df)
                num += w_t_d
                den += w_t_d ** 2

            # ltn score normalized
            scores[doc.id] = num / sqrt(den)

        return scores
        
