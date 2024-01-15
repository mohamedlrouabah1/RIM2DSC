from __future__ import annotations
import pickle
#import hickle as hkl

from xml.dom import minidom
from sys import stderr
from tqdm import tqdm

from models.txt.TextCollection import TextCollection
from models.xml.XMLDocument import XMLDocument
from models.xml.XMLIndexer import XMLIndexer
from models.xml.XMLPreprocessor import XMLPreprocessor

class XMLCollection(TextCollection):
    """
    Implementation of the XMLCollection class to handle a collection of XML documents.

    Attributes:
    -----------
    - collection: list of XMLDocument
        List to store XMLDocument objects representing the XML documents in the collection.
    - terms_frequency: dict
        Dictionary to store the frequency of terms in the collection.
    - vocabulary_size: int
        Total number of unique terms in the collection.
    - preprocessor: XMLPreprocessor
        Preprocessor for XML documents.
    - indexer: XMLIndexer
        Indexer for XML documents.
    - information_retriever: None
        Placeholder for an information retriever instance.

    Methods:
    --------
    - load() -> list[tuple[str, minidom.Document]]:
        Load the collection from a file and return a list of tuples containing document ids and minidom.Documents.
    - preprocess(raw_collection: list[tuple[str, minidom.Document]]) -> None:
        Preprocess the raw XML collection using the XMLPreprocessor.
    - index() -> None:
        Index the preprocessed XML collection using the XMLIndexer.
    - compute_stats() -> dict[int]:
        Compute various collection statistics.
    - _compute_avdl() -> float:
        Compute the average document length in the collection.
    - _compute_avtl() -> float:
        Compute the average token length in the collection.
    - _compute_terms_collection_frequency() -> list[float]:
        Compute the collection frequency of each term in the collection.
    - _compute_nb_distinct_terms() -> None:
        Compute the number of distinct terms in each document and average over the collection.
    - compute_RSV(query: str, col_type: str = "xml") -> list[str, float]:
        Compute the Relevant Status Value (RSV) of documents for a query.
    - serialize(path: str) -> bool:
        Serialize the indexed collection and save it to a file.
    - deserialize(path: str) -> 'XMLCollection':
        Deserialize a previously serialized XMLCollection object.

    """

    def __init__(self, path="", indexer=None, preprocessor=None, use_parallel_computing=False):
        super().__init__(path, {}, use_parallel_computing)
        self.collection:list[XMLDocument] = []
        self.terms_frequency:dict[str, int] = {}
        self.vocabulary_size = 0
        self.preprocessor = XMLPreprocessor() if preprocessor is None else preprocessor
        self.indexer = XMLIndexer() if indexer is None else indexer
        self.information_retriever = None

    def load(self) -> list[tuple[str, minidom.Document]]:
        """
        Load the collection from a file and return a list of tuples
        containing document ids and minidom.Documents.

        Returns:
        --------
        list[tuple[str, minidom.Document]]:
        List of tuples containing document ids and minidom.Documents.

        """
        print(f"Loading collection from file {self.path} ...", file=stderr)
        self.Timer.start("load_collection")
        raw_xml_collection = self.preprocessor.load(self.path)
        self.Timer.stop()
        print(f"Collection loaded in {self.Timer.get_time('load_collection')} seconds.", file=stderr)
        return raw_xml_collection

    def preprocess(self, raw_collection:list[tuple[str, minidom.Document]]) -> None:
        """
        Preprocess the raw XML collection using the XMLPreprocessor.

        Params:
        -------
        raw_collection: list[tuple[str, minidom.Document]]
            List of tuples containing document ids and minidom.Documents.

        Returns:
        --------
        None

        """
        print("Preprocessing collection...", file=stderr)
        self.Timer.start("preprocessing")
        self.collection = self.preprocessor.pre_process(raw_collection, self.use_parallel_computing)
        self.Timer.stop()
        print(f"Collection of {len(self.collection)} documents, preprocessed in {self.Timer.get_time('preprocessing')} seconds.", file=stderr)
        print(f"Number of anchors list find : {len(XMLPreprocessor.anchors)}", file=stderr)

    def index(self) -> None:
        print("Indexing collection...", file=stderr)
        self.Timer.start("indexing")
        self.indexer.index(self.collection, self.use_parallel_computing)
        self.Timer.stop()
        print(f"Collection indexed in {self.Timer.get_time('indexing')} seconds.", file=stderr)

    def compute_stats(self) -> dict[int]:
        """
        Compute various collection statistics sush as :
        - average document length
        - average token length
        - collection frequency of each term
        - number of distinct terms in each document and average over the collectionEE
        """
        print("Computing collection statistics...", file=stderr)
        self.Timer.start("compute_statistics")
        print("computing avdl ...", file=stderr)
        self.avdl = self._compute_avdl()
        self.indexer.avdl = self.avdl
        print("computing avtl ...", file=stderr)
        self.avtl = self._compute_avtl()
        print("computing terms collection frequency ...", file=stderr)
        self.cf = self._compute_terms_collection_frequency()
        self.Timer.stop()
        print("computing nb distinct terms ...", file=stderr)
        self._compute_nb_distinct_terms()
        print(f"Collection statistics computed in {self.Timer.get_time('compute_statistics')} seconds.", file=stderr)

    def _compute_avdl(self) -> float:
        return sum(len(d) for d in self.collection) / len(self.collection)

    def _compute_avtl(self) -> float:
        return sum(doc.compute_avtl() for doc in tqdm(self.collection, desc="Computing avtl ...")) / len(self.collection)

    def _compute_terms_collection_frequency(self) -> list[float]:
        return [self.indexer.get_df(term) for term in self.indexer.get_vocabulary()]

    def _compute_nb_distinct_terms(self) -> None:
        tot = 0
        self.indexer.nb_distinct_terms = {}
        for doc in tqdm(self.collection, desc="Computing nb distinct terms ..."):
            tokens = doc.get_text_content()
            nb_distinct_terms = len(set(tokens))
            tot += nb_distinct_terms
            self.indexer.nb_distinct_terms[doc.id] = nb_distinct_terms

        self.indexer.average_nb_distinct_terms = tot / len(self.collection)
        print(f"Average nb distinct terms: {self.indexer.average_nb_distinct_terms}, (XMLCollection._compute_nb_distinct_terms)", file=stderr)


    def compute_RSV(self, query:str, col_type="xml") -> list[str, float]:
        """
        Compute the Relevant Status Value (RSV) of documents for a query.

        Params:
        -------
        query: str
            Query string.
        col_type: str, optional
            Collection type, "xml" or other.

        Returns:
        --------
        list[str, float]: List of tuples containing document ids and RSV scores,
                          sorted by doc id.

        """
        if col_type == "xml":
            collection = []
            for doc_xml in tqdm(self.collection, desc="Extracting XML elements from documents ...."):
                collection  += doc_xml.get_xml_element_list()

        else:
            collection = self.collection

        print(f"Computing RSV for {len(collection)} xpath...")
        scores = self.information_retriever.compute_scores(collection, query, self.indexer)
        return sorted(scores.items(), key=lambda x: (x[0], x[1]), reverse=False)


    def serialize(self, path:str) -> bool:
        try:
            print(f"Serializing indexed collection to {path} ...", file=stderr)
            # hkl.dump(self, path, mode="w", compression="gzip")
            with open(path, 'wb') as f:
                pickle.dump(self, f)
            print("Indexed collection serialized to", path, file=stderr)
            return True

        except Exception as e:
            print(f"Error serializing indexed collection to {path}: {e}", file=stderr)
            return False

    @classmethod
    def deserialize(cls, path:str) -> 'XMLCollection' :
        with open(path, 'rb') as f:
            xml_collection = pickle.Unpickler(f).load()
        # xml_collection = hkl.load(path)

        if not isinstance(xml_collection, cls):
            print(f"Deserialized object from {path} is not an instance of the xml_collection class.", file=stderr)
            return None

        return xml_collection
