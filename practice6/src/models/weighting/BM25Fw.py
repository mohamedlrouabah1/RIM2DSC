from models.weighting.BM25 import BM25
from models.xml.XMLDocument import XMLDocument

class BM25Fw(BM25):
    def compute_scores(self, documents, query, indexer) -> dict[str, float]:
        """
        We ponderate BM25 tag weights according to weigh define in
        the XMLDocument.granularity_weights dictionary : dict[tag] = weight.
        """
        bm25_scores = super().compute_scores(documents, query, indexer)
        scores = {}

        for doc_id_xpath, score in bm25_scores.items():
            doc_id, xpath = doc_id_xpath.split(':')
            current_tag = xpath.split('/')[-1]

            weighted_score = XMLDocument.granularity_weights[current_tag] * score

            if doc_id not in scores:
                scores[doc_id] = weighted_score
            else:
                scores[doc_id] += weighted_score

        return scores