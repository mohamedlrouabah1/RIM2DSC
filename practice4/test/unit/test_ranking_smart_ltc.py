from pytest import approx
from models.weighting.SMART_ltc import SMART_ltc

from unit.test_data.TD3TestData import TD3TestData

class TestSmartLtc:
    data = TD3TestData()
    smart_ltc = SMART_ltc(data.N)

    def test_instantiation(self):
        smart_ltc = TestSmartLtc.smart_ltc
        data = TestSmartLtc.data
        assert smart_ltc.smart_ltn is not None
        assert smart_ltc.smart_ltn.N == data.N

    def test_compute_score(self):
        smart_ltc = TestSmartLtc.smart_ltc
        data = TestSmartLtc.data
        query = data.get_test_query()
        collection = data.get_test_collection()
        collection.set_ranking_function(smart_ltc)
        scores = collection.RSV(query)

        for doc in collection.documents:
            _, computed_score = scores[doc.id]
            expected_score = data.RSV_smart_ltc[doc.id]
            assert computed_score == approx(expected_score, abs=data.APPROX), f"collection: {collection}, doc: {doc}, expected: {expected_score}, actual: {computed_score}"