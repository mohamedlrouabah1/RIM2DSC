from functools import lru_cache
from math import log10
from models.weighting.BM25 import BM25

class BM25L(BM25):
    """
    BM25 Okapi weighting function implementation.

    Additional Attributes:
        - k3 (float, optional): Parameter controlling term frequency saturation. Defaults to 1.0.

    Methods:
        __init__(N, avdl, k1=1.2, b=0.75, k3=1.0): Initializes the BM25 Okapi weighting function with collection parameters.
        compute_tf_weight_tf_part(tf: float) -> tuple: Computes the numerator and denominator parts related to term frequency in the BM25 Okapi formula.
    """

    def __init__(self, N, avdl, k1=1.2, b=0.75, k3=1.0):
        """
        Initializes the BM25 Okapi weighting function with collection parameters.

        Params:
        -------
        N (int): Number of documents in the collection.
        avdl (float): Average document length.
        k1 (float, optional): Parameter controlling term saturation. Defaults to 1.2.
        b (float, optional): Parameter controlling length normalization. Defaults to 0.75.
        k3 (float, optional): Parameter controlling term frequency saturation. Defaults to 1.0.
        """
        super().__init__(N, avdl, k1, b)
        self.k3 = k3

    @lru_cache(maxsize=1024)
    def compute_tf_weight_tf_part(self, tf: float) -> tuple:
        """
        Computes the numerator and denominator parts related to term frequency in the BM25 Okapi formula.

        Params:
        -------
        tf (float): Term frequency in the document.

        Returns:
        --------
        tuple: Tuple containing the numerator and denominator parts.

        """
        k1_times_tf = self.k1 * tf
        tf_num = k1_times_tf * (self.k3 + 1)
        tf_den = k1_times_tf + self.k3
        return tf_num, tf_den

    def compute_weight(self, tf: float, df: float, dl: int) -> float:
        """
        Computes the BM25 Okapi weight for a term in a document.

        Params:
        -------
        tf (float): Term frequency in the document.
        df (float): Document frequency of the term.
        dl (float): Document length.

        Returns:
        --------
        float: Computed BM25 Okapi weight.

        """
        idf = self.compute_idf_part(df)
        tf_num, tf_den = self.compute_tf_weight_tf_part(tf)
        tf_den_dl = tf_den + self.compute_tf_weight_dl_part(dl)
        try:
            tf_weight = tf_num / tf_den_dl
        except ZeroDivisionError:
            tf_weight = 0
        return tf_weight * idf
