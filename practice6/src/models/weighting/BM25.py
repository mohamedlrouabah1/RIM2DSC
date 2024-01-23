from functools import lru_cache
from math import log10
from models.weighting.WeightingFunction import WeightingFunction

class BM25(WeightingFunction):
    """
    BM25 weighting function implementation.

    Attributes:
        - N (int): Number of documents in the collection.
        - avdl (float): Average document length.
        - k1 (float, optional): Parameter controlling term saturation. Defaults to 1.2.
        - b (float, optional): Parameter controlling length normalization. Defaults to 0.75.

    Methods:
        __init__(N, avdl, k1=1.2, b=0.75): Initializes the BM25 weighting function with collection parameters.
        compute_idf_part(df: float) -> float: Computes the IDF part of the BM25 formula.
        compute_tf_weight_tf_part(tf: float) -> tuple: Computes the numerator and denominator parts related to term frequency in the BM25 formula.
        compute_tf_weight_dl_part(dl: float) -> float: Computes the part related to document length in the BM25 formula.
        compute_weight(tf: float, df: float, dl: float) -> float: Computes the BM25 weight for a term in a document.
        compute_scores(documents, query, indexer) -> dict[str, float]: Computes BM25 scores for each document based on a given query.

    """

    def __init__(self, N, avdl, k1=1.2, b=0.75):
        """
        Initializes the BM25 weighting function with collection parameters.

        Params:
        -------
        N (int): Number of documents in the collection.
        avdl (float): Average document length.
        k1 (float, optional): Parameter controlling term saturation. Defaults to 1.2.
        b (float, optional): Parameter controlling length normalization. Defaults to 0.75.

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
    def compute_idf_part(self, df:float) -> float:
        """
        Params:
            df: int, document frequency of the term
        """
        return log10((self.N_plus_0_5 - df ) / (df + 0.5))

    @lru_cache(maxsize=1024)
    def compute_tf_weight_tf_part(self, tf: float) -> tuple[float]:
        return (tf * self.k1_plus_1, self.k1_times_1_minus_b + tf)

    @lru_cache(maxsize=1024)
    def compute_tf_weight_dl_part(self, dl:int) -> float:
        return (float)(self.k1_times_b_times_inv_avdl * dl)

    @lru_cache(maxsize=1024)
    def compute_weight(self, tf:float, df:float, dl:int) -> float:
        """
        Computes the BM25 weight for a term in a document.

        Params:
        -------
        tf (float): Term frequency in the document.
        df (float): Document frequency of the term.
        dl (float): Document length.

        Returns:
        --------
        float: Computed BM25 weight.

        """
        idf = self.compute_idf_part(df)
        tf_num, tf_den = self.compute_tf_weight_tf_part(tf)
        tf_den_dl = tf_den + self.compute_tf_weight_dl_part(dl)

        tf_weight = tf_num / tf_den_dl if tf_den_dl != 0 else 1

        return tf_weight * idf

    def compute_scores(self, documents, query, indexer) -> dict[str, float]:
        """
        Computes BM25 scores for each document based on a given query.

        Params:
        -------
        documents: list of TextDocument
            List of documents to compute scores for.
        query: list of str
            Query terms.
        indexer: TextIndexer
            Text indexer containing document statistics.

        Returns:
        --------
        dict[str, float]: Dictionary of scores for each document, where keys are document ids.

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
