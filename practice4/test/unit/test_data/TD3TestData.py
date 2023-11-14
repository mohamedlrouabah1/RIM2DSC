from models.Document import Document
from models.Collection import Collection

class TD3TestData:
    def __init__(self):
        self.APPROX = 1e-4
        self.N = 1000
        self.avdl = 20
        self.k1 = 1.0
        self.b = 0.5
        self.documents = [1, 2]
        self.idf = {'a': 2.0, 'b': 1.6, 'c': 2.0, 'd': 1.62, 'e': 0.6}
        self.count_matrix = {
            1: {'a': 1.0, 'b': 0.0, 'c': 1.0, 'd': 4.0, 'e': 5.0, 'dl': 11},
            2: {'a': 1.0, 'b': 4.0, 'c': 1.0, 'd': 0.0, 'e': 0.0, 'dl': 6}
        }
        # term frequencey : tft,d  = 1+log​(tf) 				
        self.tf_t_d = {
            'a': {1: 1.0000, 2: 1.0000},
            'b': {1: 0.0000, 2: 1.6021},
            'c': {1: 1.0000, 2: 1.0000},
            'd': {1: 1.6021, 2: 0.0000},
            'e': {1: 1.6990, 2: 0.0000},
            'dl': {1: 5.3010, 2: 3.6021}
        }
        # document frequency
        self.dft = {
            'a': 10.00,
            'b': 25.00,
            'c': 10.00,
            'd': 24.00,
            'e': 250.00
        }
        # ranking : SMART ltn
        self.weights_smart_ltn = {
            'a': {1: 2.0000, 2: 2.0000},
            'b': {1: 0.0000, 2: 2.5666},
            'c': {1: 2.0000, 2: 2.0000},
            'd': {1: 2.5950, 2: 0.0000},
            'e': {1: 1.0229, 2: 0.0000}
        }
        self.RSV_smart_ltn = {1: 3.0229, 2: 2.0000}
        # ranking : SMART ltc
        self.weights_smart_ltc = {
            'a': {1: 0.5035, 2: 0.5236},
            'b': {1: 0.0000, 2: 0.6720},
            'c': {1: 0.5035, 2: 0.5236},
            'd': {1: 0.6533, 2: 0.0000},
            'e': {1: 0.2575, 2: 0.0000}
        }
        self.RSV_smart_ltc = {1: 0.7610, 2: 0.5236}
        # ranking : BM25
        self.weights_bm25_tf_part = {
            'a': {1: 1.1268, 2: 1.2121},
            'b': {1: 0.0000, 2: 1.7204},
            'c': {1: 1.1268, 2: 1.2121},
            'd': {1: 1.6754, 2: 0.0000},
            'e': {1: 1.7316, 2: 0.0000}
        }
        self.weights_bm25_df_part = {
            'a': 1.9747,
            'b': 1.5827,
            'c': 1.9747,
            'd': 1.6005,
            'e': 0.4765
        }
        self.weights_bm25 = {
            'a': {1: 2.2250, 2: 2.3935},
            'b': {1: 0.0000, 2: 2.7229},
            'c': {1: 2.2250, 2: 2.3935},
            'd': {1: 2.6815, 2: 0.0000},
            'e': {1: 0.8252, 2: 0.0000},
        }
        self.RSV_bm25 = {1: 3.0502, 2: 2.3935}


    def get_test_collection(self):
        collection = Collection()
        collection.documents = [
            Document(1, "c d d d e e e e a d e"),
            Document(2, "a b b b b c")
        ]
        collection.compute_index(save=False)
        collection.compute_statistics()
        return collection

    def get_test_query(self):
        return "a e"