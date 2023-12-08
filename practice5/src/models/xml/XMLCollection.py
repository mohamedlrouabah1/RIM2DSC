from sys import stderr
from types import Any

import xml.dom.minidom as minidom

from models.concepts.CollectionOfRessources import CollectionOfRessources
from models.xml.XMLDocument import XMLDocument
from models.xml.XMLIndexer import XMLIndexer
from models.xml.XMLPreprocessor import XMLPreprocessor
from models.Timer import Timer

class XMLCollection(CollectionOfRessources):

    def __init__(self, path:str, indexer=None, preprocessor=None, use_parallel_computing=False):
        super().__init__(path, {})
        self.documents:list(XMLDocument) = []
        self.terms_frequency:dict(str, int) = {}
        self.vocabulary_size = 0
        self.path = path
        self.Timer = Timer()
        self.preprocessor = XMLPreprocessor() if preprocessor is None else preprocessor
        self.indexer = XMLIndexer() if indexer is None else indexer
        self.information_retriever = None
        self.use_parallel_computing = use_parallel_computing

    def load(self) -> list(tuple(str, minidom.Document)):
        print(f"Loading collection from file {self.path} ...", file=stderr)
        self.Timer.start("load_collection")
        raw_xml_collection = self.preprocessor.load(self.path)
        self.Timer.stop()
        print(f"Collection loaded in {self.Timer.get_time('load_collection')} seconds.", file=stderr)
        return raw_xml_collection

    def preprocess(self, raw_collection) -> None:
        print("Preprocessing collection...", file=stderr)
        self.Timer.start("preprocessing")
        self.documents = self.preprocessor.pre_process(raw_collection, self.use_parallel_computing)
        self.Timer.stop()
        print(f"Collection preprocessed in {self.Timer.get_time('preprocessing')} seconds.", file=stderr)

    def index(self) -> None:
        raise NotImplementedError("Should implement indexing()")
    
    def compute_RSV(self, query:str) -> dict(int):
        raise NotImplementedError("Should implement query()")
    
    def compute_stats(self) -> dict(int):
        raise NotImplementedError("Should implement compute_stats()")