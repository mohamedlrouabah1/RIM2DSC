from pytest import approx
from models.weighting.BM25 import BM25
from models.Document import Document
from models.Indexer import Indexer
from models.Collection import Collection
from unit.test_data.TD3TestData import TD3TestData


class TestBM25:
    data = TD3TestData()
    bm25 = BM25(data.N, data.avdl, data.k1, data.b)

    def test_instantiation(self):
        bm25 = TestBM25.bm25
        data = TestBM25.data
        assert bm25.N == data.N
        assert bm25.avdl == data.avdl
        assert bm25.k1 == data.k1
        assert bm25.b == data.b
        assert bm25.k1_plus_1 == data.k1 + 1
        assert bm25.k1_times_1_minus_b == data.k1 * (1 - data.b)
        assert bm25.k1_times_b_times_inv_avdl == data.k1 * data.b / data.avdl
        assert bm25.N_plus_0_5 == data.N + 0.5

    def test_compute_weight(self):
        bm25 = TestBM25.bm25
        data = TestBM25.data
        for term, result_weight in data.weights_bm25.items():
            for doc_id in data.documents:
                weight = bm25.compute_weight(
                    data.tf_t_d[term][doc_id], 
                    data.dft[term], 
                    data.count_matrix[doc_id]['dl']
                    )
                computed_weight = round(weight, 4)
                expected_weight = round(result_weight[doc_id], 4)
                assert  computed_weight == approx(expected_weight, abs=data.APPROX), f"Term: {term}, Doc_id: {doc_id}, Expected: {expected_weight}, Actual: {computed_weight}"
                
    def test_compute_score(self):
        bm25 = TestBM25.bm25
        data = TestBM25.data
        query = data.get_test_query()
        collection = data.get_test_collection()
        collection.set_ranking_function(bm25)
        scores = collection.RSV(query)

        for doc in collection.documents:
            _, computed_score = scores[doc.id]
            expected_score = data.RSV_bm25[doc.id]
            assert computed_score == expected_score
        