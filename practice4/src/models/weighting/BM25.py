from math import log10
from WeightingFunction import WeightingFunction

class SMART_ltn(WeightingFunction):

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


    
    # TODO optimize this computation by computing the idf outside and not for each document 
    def compute_score(self, tf, df, dl):
        """
        tf: term frequency in the document
        df: document frequency of the term
        dl: document length
        """
        # TODO : remove the if  for idf
        # TODO : compute the idf outside for not recomputing it for each document bc depend on the collection and not the document neither the term.
        # thus it prevent to compute it for each document and save time
        idf = log10((self.N_plus_0_5 - df ) / (df + 0.5)) if df > 0 else 0
        tf_weight = (tf * self.k1_plus_1) / (self.k1_times_1_minus_b + self.k1_times_b_times_inv_avdl * dl + tf)
        return tf_weight * idf
    
        # TODO make an alternative function that compute log(a) -log(b) instead of log(a/b)
        # and see which one is the fastest.