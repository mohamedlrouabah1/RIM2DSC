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
                _, xpath = doc.id.split(':')
                current_tag = xpath.split('/')[-1]
                df = indexer.get_df(term)
                tf = indexer.get_tf(term, doc.id) * XMLDocument.granularity_weights[current_tag]
                dl = len(doc)
                score += self.compute_weight(tf, df, dl)
            scores[doc.id] = score

        return scores
