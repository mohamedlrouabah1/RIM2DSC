from sys import stderr
from functools import lru_cache
from math import log10, sqrt
from models.weighting.SMART_ltn import SMART_ltn
from models.weighting.WeightingFunction import WeightingFunction


class SMART_lnu(WeightingFunction):

    def __init__(self, N, slope):
        self.N = N
        self.slope = slope

    def _compute_weight(self, tf, dl_on_avdl, nt_d, den_part1) -> float:
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

    def compute_scores(self, documents, query, indexer):
        scores = {}
        avdl = indexer.avdl
        pivot = indexer.average_nb_distinct_terms
        den_part1 = (1 - self.slope) * pivot
        for doc in documents:
            score = 0
            dl_on_avdl = len(doc) / avdl
            nt_d = indexer.nb_distinct_terms[doc.id.split(':')[0]]
            for term in query:
                df = indexer.get_df(term)
                tf = indexer.get_tf(term, doc.id)
                score += self._compute_weight(tf, dl_on_avdl, nt_d, den_part1)
            scores[doc.id] = score

        return scores