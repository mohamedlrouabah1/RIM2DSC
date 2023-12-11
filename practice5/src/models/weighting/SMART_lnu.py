from sys import stderr
from functools import lru_cache
from math import log10, sqrt
from models.weighting.SMART_ltn import SMART_ltn
from models.weighting.WeightingFunction import WeightingFunction


class SMART_lnu(WeightingFunction):

    def __init__(self, N, slope):
        self.N = N
        self.slope = slope

    def _compute_weight(self, tf, dl_on_avdl, nt_d, den_part1):
        num = 1 + log10(tf)
        num /= 1 + log10(dl_on_avdl)
        den = den_part1 + self.slope * nt_d


    def compute_scores(self, documents, query, indexer):
        avdl = indexer.get_avdl()
        pivot = indexer.average_nb_distinct_terms
        den_part1 = (1 - self.slope) * pivot
        for doc in documents:
            doc.score = 0
            dl_on_avdl = doc.get_length() / avdl
            nt_d = doc.nb_distinct_terms
            for term in query:
                df = indexer.get_df(term)
                tf = indexer.get_tf(term, doc.id)
                doc.score += self._compute_weight(tf, dl_on_avdl, nt_d, den_part1)