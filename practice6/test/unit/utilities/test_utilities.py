import unittest
from unittest.mock import patch

from utilities.utilities import *

class ARGS :
    """A class to store some attributes"""
    def __init__(self) -> None:
        pass
class TestUtilities(unittest.TestCase):

    @patch('models.txt.TextCollection.TextCollection')
    @patch('models.txt.TextIndexer.TextIndexer')
    @patch('models.txt.TextPreprocessor.TextPreprocessor')
    def test_create_or_load_collection_txt(self):
        self._set_global_context()
        args = self._create_args()

        txt_collection = create_or_load_collection(args, type="txt", save=False)
        self.assertIsNotNone(txt_collection)
        self.assertIsInstance(txt_collection, TextCollection)

    @patch('models.xml.XMLCollection.XMLCollection')
    @patch('models.xml.XMLIndexer.XMLIndexer')
    @patch('models.xml.XMLPreprocessor.XMLPreprocessor')
    def test_create_or_load_collection_xml(self):
        self._set_global_context()
        args = self._create_args()

        xml_collection = create_or_load_collection(args, type="xml", save=False)
        self.assertIsNotNone(xml_collection)
        self.assertIsInstance(xml_collection, XMLCollection)


    def test_load_queries_from_csv_incorrect_path(self):
        self.assertRaises(FileNotFoundError, load_queries_from_csv, "incorrect_path")

    def test_load_queries_from_csv_correct_path(self):
        queries = load_queries_from_csv("data/practice_6/queries.csv")
        self.assertEqual(len(queries), 7)
        

    def test_launch_run(self):
        self.assertIsNotNone(launch_run)


    def _set_global_context(self) -> None:
        global SAVE_FOLDER, COLLECTION_NAME, DATA_PRACTICE_5
        SAVE_FOLDER = '.pytest_cache/test_utilities/'
        COLLECTION_NAME = 'test_collection'
        DATA_PRACTICE_5 = "data/Practice_05_data/XML-Coll-withSem/"

    def _create_args(self) -> ARGS:
        args = ARGS()
        args.tokenizer = "nltk"
        args.lemmer = True
        args.parallel_computing = False
        args.generate_index = True
        args.stopword = True
        args.stemmer = "porter"

        return args