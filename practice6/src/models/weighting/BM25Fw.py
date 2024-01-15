from __future__ import annotations

from models.weighting.BM25 import BM25
from models.xml.XMLDocument import XMLDocument

class BM25Fw(BM25):
    """
    Implementation of BM25 weighting function for XML documents with late combinaison
    of tags.

     Methods:
        compute_scores(documents, query, indexer) -> dict[str, float]:
        Computes BM25 scores for each document based on a given query, considering
        XMLDocument granularity weights.

    """

    def compute_scores(self, documents, query, indexer) -> dict[str, float]:
        """
        We ponderate BM25 tag weights according to weigh define in
        the XMLDocument.granularity_weights dictionary : dict[tag] = weight.

        Params:
        -------
        documents: list of XMLDocument
            List of XML documents to compute scores for.
        query: list of str
            Query terms.
        indexer: TextIndexer
            Text indexer containing document statistics.

        Returns:
        --------
        dict[str, float]: Dictionary of scores for each document,
                          where keys are document ids.

        """
        bm25_scores = super().compute_scores(documents, query, indexer)
        scores = {}

        for doc_id_xpath, score in bm25_scores.items():
            doc_id, xpath = doc_id_xpath.split(':')
            current_tag = xpath.split('/')[-1].split('[')[0]

            weighted_score = XMLDocument.granularity_weights[current_tag] * score

            doc_id = f"{doc_id}:/article[1]"
            if doc_id not in scores:
                scores[doc_id] = weighted_score
            else:
                scores[doc_id] += weighted_score

        return scores