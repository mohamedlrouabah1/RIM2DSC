from functools import lru_cache
from math import sqrt

from models.concepts.InformationRessource import InformationRessource
from models.txt.TextIndexer import TextIndexer
from models.weighting.SMART_ltn import SMART_ltn
from models.weighting.WeightingFunction import WeightingFunction

class SMART_ltc(WeightingFunction):
    """
    Implementation of the SMART_ltc weighting function.

    Methods:
        compute_scores(documents, query, indexer) -> dict[str, float]:
        Computes SMART_ltc scores for each document based on a given query and a text indexer.

    """

    def __init__(self, N, **kargs):
        """
        Initialize the SMART_ltc weighting function.

        Params:
        -------
        N: int
            Number of documents in the collection.
        kargs: dict
            Keyword arguments, including 'smart_ltn' for
            specifying SMART_ltn weighting function instance.

        """
        if  'smart_ltn' in kargs:
            self.smart_ltn = kargs['smart_ltn']
        else:
            self.smart_ltn = SMART_ltn(N)

    def compute_scores(self, documents:list[InformationRessource], query:list[str], indexer:TextIndexer) -> dict[str, float]:
        """
        Computes SMART_ltc scores for each document based on a given query and a text indexer.

        Params:
        -------
        documents: list of InformationRessource
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
        # compute the denominator used to normalise ltn weights depending on document
        dens = {}
        vocab = indexer.posting_lists.values()
        for posting_list in vocab:
            df = posting_list.document_frequency
            for doc_id, posting_unit in posting_list.postings.items():
                # NB : here we only considering the root node of the doc
                doc_id, xpath = doc_id.split(':')
                if xpath == '/article[1]':
                    tf = posting_unit.frequency
                    if doc_id in dens:
                        dens[doc_id] += self.smart_ltn.compute_weight(tf, df) ** 2

                    else:
                        dens[doc_id] = self.smart_ltn.compute_weight(tf, df) ** 2

        # Compute ltn for each document
        for doc in documents:
            deno, num = 0, 0
            for term in query:
                df = indexer.get_df(term)
                tf = indexer.get_tf(term, doc.id)

                w_t_d = self.smart_ltn.compute_weight(tf, df)
                num += w_t_d

            # ltn score normalized
            if doc.id.find(':') != -1:
                doc_id, _ = doc.id.split(':')
            else:
                doc_id = doc.id
            deno = dens[doc_id] if doc_id in dens else 1
            deno = sqrt(deno) if deno != 0 else 1
            scores[doc.id] = num / deno

        return scores

    @lru_cache(maxsize=1024)
    def _compute_weight(self, ltn_list, tf_list, index):
        """
        Compute the SMART_ltc weight.

        Params:
        -------
        ltn_list: list of float
            List of SMART_ltn weights for terms in the query.
        tf_list: list of float
            List of term frequencies for terms in the query.
        index: list of int
            List of indices of terms in the query.

        Returns:
        --------
        float: SMART_ltc weight.

        """
        den, num = 0, 0
        for i, (ltn, _) in enumerate(zip(tf_list, ltn_list)):
            den += ltn ** 2
            if i in index:
                print(f"i: {i}, w_t_d: {ltn}")
                num += ltn

        return num / sqrt(den)
