from sys import stderr
from typing import Any

import xml.dom.minidom as minidom

from models.concepts.CollectionOfRessources import CollectionOfRessources
from models.xml.XMLDocument import XMLDocument
from models.xml.XMLIndexer import XMLIndexer
from models.xml.XMLPreprocessor import XMLPreprocessor
from models.Timer import Timer

class XMLCollection(CollectionOfRessources):

    def __init__(self, path:str, indexer=None, preprocessor=None, use_parallel_computing=False):
        super().__init__(path, {}, use_parallel_computing)
        self.documents:list(XMLDocument) = []
        self.terms_frequency:dict(str, int) = {}
        self.vocabulary_size = 0
        self.preprocessor = XMLPreprocessor() if preprocessor is None else preprocessor
        self.indexer = XMLIndexer() if indexer is None else indexer
        self.information_retriever = None

    def load(self) -> list[tuple[str, minidom.Document]]:
        print(f"Loading collection from file {self.path} ...", file=stderr)
        self.Timer.start("load_collection")
        raw_xml_collection = self.preprocessor.load(self.path)
        self.Timer.stop()
        print(f"Collection loaded in {self.Timer.get_time('load_collection')} seconds.", file=stderr)
        return raw_xml_collection

    def preprocess(self, raw_collection:list[tuple[str, minidom.Document]]) -> None:
        print("Preprocessing collection...", file=stderr)
        self.Timer.start("preprocessing")
        self.documents = self.preprocessor.pre_process(raw_collection, self.use_parallel_computing)
        self.Timer.stop()
        print(f"Collection of {len(self.documents)} documents, preprocessed in {self.Timer.get_time('preprocessing')} seconds.", file=stderr)

    def index(self) -> None:
        print("Indexing collection...", file=stderr)
        self.Timer.start("indexing")
        self.indexer.index(self.documents, self.use_parallel_computing)
        self.Timer.stop()
        print(f"Collection indexed in {self.Timer.get_time('indexing')} seconds.", file=stderr)
    

    def compute_RSV(self, query:str) -> dict[str, float]:
        """
        compute the Relevant Status Value of a document for a query
        """
        scores = self.information_retriever.compute_scores(self.documents, query, self.indexer)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    def compute_stats(self) -> dict[int]:
         # Compute collection statistics
        print("Computing collection statistics...", file=stderr)
        self.Timer.start("compute_statistics")
        self.avdl = self._compute_avdl()
        self.avtl = self._compute_avtl()
        self.cf = self._compute_terms_collection_frequency()
        self.Timer.stop()
        print(f"Collection statistics computed in {self.Timer.get_time('compute_statistics')} seconds.", file=stderr)

    def _compute_avdl(self) -> float:
        return sum(len(d) for d in self.documents) / len(self.documents)
    
    def _compute_avtl(self) -> float:
        return sum(doc.compute_avtl() for doc in self.documents) / len(self.documents)
    
    def _compute_terms_collection_frequency(self) -> list[float]:
        return [self.indexer.get_df(term) for term in self.indexer.get_vocabulary()]