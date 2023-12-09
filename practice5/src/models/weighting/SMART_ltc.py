from sys import stderr
from functools import lru_cache
from math import log10, sqrt
from models.weighting.SMART_ltn import SMART_ltn
from models.weighting.WeightingFunction import WeightingFunction

class SMART_ltc(WeightingFunction):

    def __init__(self, N, **kargs):
        if  'smart_ltn' in kargs:
            self.smart_ltn = kargs['smart_ltn']
        else:
            self.smart_ltn = SMART_ltn(N)

    def compute_scores(self, documents, query, indexer):
        """
        Return a dictionary of scores for each document for each query.
        The keys of the dictionary are the queries ids.
        """        
        scores = {}
        # compute the denominator used to normalise ltn weights depending on document
        dens = {}
        vocab = indexer.posting_lists.values()
        for posting_list in vocab:
            df = posting_list.document_frequency
            for doc_id, posting_unit in posting_list.postings.items():
                # NB : here we exclude the id corresponding to an XLMElement
                if doc_id.find(":") == -1:
                    tf = posting_unit.frequency
                    if posting_unit.document_id in dens:
                        dens[posting_unit.document_id] += self.smart_ltn.compute_weight(tf, df) ** 2
                    
                    else:
                        dens[posting_unit.document_id] = self.smart_ltn.compute_weight(tf, df) ** 2
       
        # Compute ltn for each document
        for doc in documents:
            deno, num = 0, 0
            for term in query:
                df = indexer.get_df(term)
                tf = indexer.get_tf(term, doc.id)

                w_t_d = self.smart_ltn.compute_weight(tf, df)
                num += w_t_d

            # ltn score normalized
            deno = dens[doc.id] if doc.id in dens else 1
            deno = sqrt(deno) if deno != 0 else 1
            scores[doc.id] = num / deno

        return scores
