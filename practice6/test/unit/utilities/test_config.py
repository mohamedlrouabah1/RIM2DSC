import unittest
import utilities.config as config

class TestGlobalConfiguration(unittest.TestCase):
    """
    Make sure that the global configuration file is correctly written.
    """

    def test_config_variables_existence(self):
        self.assertTrue(hasattr(config, 'DATA_FOLDER'))
        self.assertTrue(hasattr(config, 'STOPWORDS_DIR'))
        self.assertTrue(hasattr(config, 'SAVE_FOLDER'))
        self.assertTrue(hasattr(config, 'RENDU_FOLDER'))
        self.assertTrue(hasattr(config, 'COLLECTION_FILES'))
        self.assertTrue(hasattr(config, 'GRAPH_FOLDER'))
        self.assertTrue(hasattr(config, 'COLLECTION_NAME'))
        self.assertTrue(hasattr(config, 'DATA_PRACTICE_5'))
        self.assertTrue(hasattr(config, 'NB_RANKING'))
        self.assertTrue(hasattr(config, 'START_TAG'))
        self.assertTrue(hasattr(config, 'RECURSION_LIM'))
    
    def test_config_variables_type(self):
        self.assertIsInstance(config.DATA_FOLDER, str)
        self.assertIsInstance(config.STOPWORDS_DIR, str)
        self.assertIsInstance(config.SAVE_FOLDER, str)
        self.assertIsInstance(config.RENDU_FOLDER, str)
        self.assertIsInstance(config.COLLECTION_FILES, list)
        self.assertIsInstance(config.GRAPH_FOLDER, str)
        self.assertIsInstance(config.COLLECTION_NAME, str)
        self.assertIsInstance(config.DATA_PRACTICE_5, str)
        self.assertIsInstance(config.NB_RANKING, int)
        self.assertIsInstance(config.START_TAG, str)
        self.assertIsInstance(config.RECURSION_LIM, int)

if __name__ == '__main__':
    unittest.main()