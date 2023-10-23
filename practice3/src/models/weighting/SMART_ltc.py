from math import log10, sqrt
from WeightingFunction import WeightingFunction
from SMART_ltn import SMART_ltn

class SMART_ltn(WeightingFunction):

    def __init__(self, smart_ltn):
        if smart_ltn is not None:
            self.smart_ltn = smart_ltn
        else:
            self.smart_ltn = SMART_ltn()
    
    # TODO: make sure a ltn weith is pass as tf for the compute_score function
    def compute_score(tf, all_tf):
        tf_prime = 1 + log10(tf) if tf > 0 else 0
        normalization = sqrt(sum((1 + log10(k)) ** 2 for k in all_tf))
        return tf_prime / normalization if normalization != 0 else 0
