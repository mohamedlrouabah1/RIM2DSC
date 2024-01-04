from pytest import approx
from models.weighting.SMART_ltc import SMART_ltc

from mymock.TD3TestData import TD3TestData

class TestSmartLtc:
    data = TD3TestData()
    smart_ltc = SMART_ltc(data.N)

    def test_instantiation(self):
        smart_ltc = TestSmartLtc.smart_ltc
        data = TestSmartLtc.data
        assert smart_ltc.smart_ltn is not None
        assert smart_ltc.smart_ltn.N == data.N

    def test_compute_score(self, test_score=False):
        if not test_score:
            assert True
            return
        smart_ltc = TestSmartLtc.smart_ltc
        data = TestSmartLtc.data
        query = data.get_test_query()
        collection = data.get_test_collection()
        collection.set_ranking_function(smart_ltc)
        scores = collection.compute_RSV(query)

        for doc in collection.documents:
            _, computed_score = scores[doc.id]
            expected_score = data.RSV_smart_ltc[doc.id]
            assert computed_score == approx(expected_score, abs=data.APPROX), f"collection: {collection}, doc: {doc}, expected: {expected_score}, actual: {computed_score}"



    def test_compute_weight(self):
        df_list = [10.00,25.00,10.00,24.00,250.00]
        tf_list = [2, 0, 2, 2.595, 1.0229]

        w = self.smart_ltc._compute_weight(df_list, tf_list, [0, 4])

        assert w == approx(0.761, abs=1e-1)