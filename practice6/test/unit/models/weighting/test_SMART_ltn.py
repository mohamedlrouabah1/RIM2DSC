from pytest import approx
from models.weighting.SMART_ltn import SMART_ltn
from test.mock.TD3TestData import TD3TestData

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
        a_d1 = self.smart_ltn.compute_weight(1, 10)  
        assert a_d1 == approx(2.0, abs=1e-1)

        b_d1 = self.smart_ltn.compute_weight(0, 25)
        assert b_d1 == approx(0.0, abs=1e-1)

        c_d1 = self.smart_ltn.compute_weight(1, 10)
        assert c_d1 == approx(2.0, abs=1e-1)

        d_d1 = self.smart_ltn.compute_weight(4, 24)
        assert d_d1 == approx(2.5950, abs=1e-1)

        e_d1 = self.smart_ltn.compute_weight(5, 250)
        assert e_d1 == approx(1.0229, abs=1e-1)

        

    def test_compute_score(self, weight=True):
        assert weight