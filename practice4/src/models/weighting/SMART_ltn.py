from functools import lru_cache
from math import log10
from WeightingFunction import WeightingFunction

class SMART_ltn(WeightingFunction):

    @lru_cache(maxsize=None)
    def compute_idf(self, df, N):
        return log10(N / df)
    
    @lru_cache(maxsize=None)
    def compute_tf_part(self, tf):
        return 1 + log10(tf)

    # TODO optimize this computation by computing the idf outside and not for each document 
    @lru_cache(maxsize=None)
    def compute_score(self, tf, df, N):
        if df > 0 and N > df:
            idf = self.compute_idf(df, N)
            tf_part = self.compute_tf_part(tf)
            return tf_part * idf
        
        return 0