from __future__ import annotations

from models.weighting.BM25 import BM25
from models.xml.XMLDocument import XMLDocument

class BM25Fr(BM25):
    def compute_scores(self, documents, query, indexer) -> dict[str, float]:
        """
        We ponderate BM25 term frequency according to weigh define in
        the XMLDocument.granularity_weights dictionary : dict[tag] = weight.
        """
        scores = {}
        for doc in documents:
            score = 0
            for term in query:
                doc_id, xpath = doc.id.split(':')
                current_tag = xpath.split('/')[-1].split('[')[0]
                df = indexer.get_df(term)
                tf = indexer.get_tf(term, doc.id) * XMLDocument.granularity_weights[current_tag]
                dl = len(doc)
                score += self.compute_weight(tf, df, dl)

            doc_id = f"{doc_id}:/article[1]"
            if doc_id not in scores:
                scores[doc_id] = score
            else:
                scores[doc_id] += score

        return scores
