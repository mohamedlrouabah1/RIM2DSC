from math import log10
from WeightingFunction import WeightingFunction

class SMART_ltn(WeightingFunction):

    # TODO optimize this computation by computing the idf outside and not for each document 
    def compute_score(self, tf, df, N):
        if df > 0 and N > df:
            return (1 + log10(tf)) * log10(N / df)
        
        return 0