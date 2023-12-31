import unittest
import os
from models.xml.XMLDocument import XMLDocument
from models.xml.XMLCollection import XMLCollection
from models.xml.XMLPreprocessor import XMLPreprocessor
from models.xml.XMLIndexer import XMLIndexer

class TestXMLCollection(unittest.TestCase):

    def setUp(self):
        self.data_path = "path/to/your/xml/data"
        self.collection_path = "path/to/your/indexed/collection.pkl"
        self.collection_indexed_path = "path/to/your/indexed/collection_indexed.pkl"
        self.preprocessor = XMLPreprocessor()
        self.indexer = XMLIndexer()

    def test_init(self):
        # Test the initialization of XMLCollection
        xml_collection = XMLCollection(path=self.data_path, indexer=self.indexer, preprocessor=self.preprocessor, use_parallel_computing=False)

        # Verify that attributes are set correctly
        self.assertEqual(xml_collection.path, self.data_path)
        self.assertEqual(xml_collection.indexer, self.indexer)
        self.assertEqual(xml_collection.preprocessor, self.preprocessor)
        self.assertEqual(xml_collection.use_parallel_computing, False)
        self.assertEqual(xml_collection.collection, [])
        self.assertEqual(xml_collection.terms_frequency, {})
        self.assertEqual(xml_collection.vocabulary_size, 0)
        self.assertIsNone(xml_collection.information_retriever)

    def test_load(self):
        # Test the load method of XMLCollection
        xml_collection = XMLCollection(path=self.data_path, indexer=self.indexer, preprocessor=self.preprocessor, use_parallel_computing=False)

        # Assume that your data is available in the specified path
        raw_xml_collection = xml_collection.load()

        # Verify that loading is successful
        self.assertIsNotNone(raw_xml_collection)
        self.assertIsInstance(raw_xml_collection, list)
        self.assertTrue(all(isinstance(item, tuple) and len(item) == 2 for item in raw_xml_collection))

    def test_preprocess(self):
        # Test the preprocess method of XMLCollection
        xml_collection = XMLCollection(path=self.data_path, indexer=self.indexer, preprocessor=self.preprocessor, use_parallel_computing=False)

        # Assume that you have a sample raw XML collection
        raw_xml_collection = [("doc1", "<xml>...</xml>"), ("doc2", "<xml>...</xml>")]

        # Preprocess the collection
        xml_collection.preprocess(raw_xml_collection)

        # Verify that preprocessing is successful
        self.assertIsNotNone(xml_collection.collection)
        self.assertIsInstance(xml_collection.collection, list)
        self.assertTrue(all(isinstance(item, XMLDocument) for item in xml_collection.collection))

    def test_index(self):
        # Test the index method of XMLCollection
        xml_collection = XMLCollection(path=self.data_path, indexer=self.indexer, preprocessor=self.preprocessor, use_parallel_computing=False)

        # Assume that you have a preprocessed XML collection
        xml_collection.collection = [XMLDocument("doc1", "<xml>...</xml>"), XMLDocument("doc2", "<xml>...</xml>")]

        # Index the collection
        xml_collection.index()

        # Verify that indexing is successful
        self.assertIsNotNone(xml_collection.indexer)
        self.assertIsInstance(xml_collection.indexer, XMLIndexer)

    def test_compute_stats(self):
        # Test the compute_stats method of XMLCollection
        xml_collection = XMLCollection(path=self.data_path, indexer=self.indexer, preprocessor=self.preprocessor, use_parallel_computing=False)

        # Assume that you have a preprocessed and indexed XML collection
        xml_collection.collection = [XMLDocument("doc1", "<xml>...</xml>"), XMLDocument("doc2", "<xml>...</xml>")]
        xml_collection.indexer = XMLIndexer()
        xml_collection.index()

        # Compute statistics
        xml_collection.compute_stats()

        # Verify that statistics are computed
        self.assertIsNotNone(xml_collection.avdl)
        self.assertIsNotNone(xml_collection.avtl)
        self.assertIsNotNone(xml_collection.cf)
        self.assertIsNotNone(xml_collection.indexer.nb_distinct_terms)
        self.assertIsNotNone(xml_collection.indexer.average_nb_distinct_terms)

    def test_compute_RSV(self):
        # Test the compute_RSV method of XMLCollection
        xml_collection = XMLCollection(path=self.data_path, indexer=self.indexer, preprocessor=self.preprocessor, use_parallel_computing=False)

        # Assume that you have a preprocessed and indexed XML collection
        xml_collection.collection = [XMLDocument("doc1", "<xml>...</xml>"), XMLDocument("doc2", "<xml>...</xml>")]
        xml_collection.indexer = XMLIndexer()
        xml_collection.index()

        # Assume that you have a sample query
        query = "sample query"

        # Compute RSV
        scores = xml_collection.compute_RSV(query)

        # Verify that scores are computed
        self.assertIsNotNone(scores)
        self.assertIsInstance(scores, list)
        self.assertTrue(all(isinstance(item, tuple) and len(item) == 2 for item in scores))

    def test_serialize_and_deserialize(self):
        # Test the serialize and deserialize methods of XMLCollection
        xml_collection = XMLCollection(path=self.data_path, indexer=self.indexer, preprocessor=self.preprocessor, use_parallel_computing=False)

        # Assume that you have a preprocessed and indexed XML collection
        xml_collection.collection = [XMLDocument("doc1", "<xml>...</xml>"), XMLDocument("doc2", "<xml>...</xml>")]
        xml_collection.indexer = XMLIndexer()
        xml_collection.index()

        # Serialize the collection
        xml_collection.serialize(self.collection_path)

        # Verify that the serialized file exists
        self.assertTrue(os.path.exists(self.collection_path))

        # Deserialize the collection
        deserialized_collection = XMLCollection.deserialize(self.collection_path)

        # Verify that deserialization is successful
        self.assertIsNotNone(deserialized_collection)
        self.assertIsInstance(deserialized_collection, XMLCollection)

        # Clean up: Remove the serialized file
        os.remove(self.collection_path)

if __name__ == "__main__":
    unittest.main()
