from pytest import approx
from models.weighting.SMART_ltn import SMART_ltn
from unit.test_data.TD3TestData import TD3TestData

class TestSmartltn:
    data = TD3TestData()
    smart_ltn = SMART_ltn(data.N)

    def test_instantiation(self):
        smart_ltn = TestSmartltn.smart_ltn
        data = TestSmartltn.data
        assert smart_ltn is not None
        assert smart_ltn.N == data.N

    def test_compute_idf(self):
        smart_ltn = TestSmartltn.smart_ltn
        data = TestSmartltn.data
        for term, result_idf in data.idf.items():
            computed_idf = smart_ltn.compute_idf(data.dft[term], data.N)
            assert computed_idf == approx(result_idf, abs=1e-1)

    def test_compute_tf_part(self, weight=True):
        assert weight
    
    def test_compute_weight(self, weight=True):
        assert weight
    
    def test_compute_score(self, weight=True):
        assert weight