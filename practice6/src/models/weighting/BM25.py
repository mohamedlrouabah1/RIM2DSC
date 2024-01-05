from functools import lru_cache
from math import log10
from models.weighting.WeightingFunction import WeightingFunction

class BM25(WeightingFunction):

    def __init__(self, N, avdl, k1=1.2, b=0.75):
        """
        N: number of documents in the collection
        avdl: average document length
        """
        super().__init__()
        self.N = N
        self.avdl = avdl
        self.k1 = k1
        self.b = b

        # store some computation values in order
        # to not recompute them at each call
        # cf formula for more details
        self.k1_plus_1 = self.k1 + 1
        self.k1_times_1_minus_b = self.k1 * (1 - self.b)
        self.k1_times_b_times_inv_avdl = self.k1 * self.b / self.avdl
        self.N_plus_0_5 = self.N + 0.5

    @lru_cache(maxsize=1024)
    def compute_idf_part(self, df):
        """
        Params:
            df: int, document frequency of the term
        """
        return log10((self.N_plus_0_5 - df ) / (df + 0.5))

    @lru_cache(maxsize=1024)
    def compute_tf_weight_tf_part(self, tf):
        return (tf * self.k1_plus_1, self.k1_times_1_minus_b + tf)

    @lru_cache(maxsize=1024)
    def compute_tf_weight_dl_part(self, dl):
        return self.k1_times_b_times_inv_avdl * dl

    @lru_cache(maxsize=1024)
    def compute_weight(self, tf, df, dl):
        """
        tf: term frequency in the document
        df: document frequency of the term
        dl: document length
        Return:
            tf_weight = (tf * self.k1_plus_1) / (self.k1_times_1_minus_b + self.k1_times_b_times_inv_avdl * dl + tf)
        """
        idf = self.compute_idf_part(df)
        tf_num, tf_den = self.compute_tf_weight_tf_part(tf)
        tf_den_dl = tf_den + self.compute_tf_weight_dl_part(dl)
        try:
            tf_weight = tf_num / tf_den_dl
        except ZeroDivisionError:
            tf_weight = 0
        return tf_weight * idf

    def compute_scores(self, documents, query, indexer) -> dict[str, float]:
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
                dl = len(doc)
                score += self.compute_weight(tf, df, dl)
            scores[doc.id] = score

        return scores
