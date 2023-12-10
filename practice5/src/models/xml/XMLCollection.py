import xml.dom.minidom as minidom
import pickle
import copy

from sys import stderr
from typing import Any
from tqdm import tqdm

from models.txt.TextCollection import TextCollection  
from models.xml.XMLDocument import XMLDocument
from models.xml.XMLIndexer import XMLIndexer
from models.xml.XMLPreprocessor import XMLPreprocessor
from models.Timer import Timer

class XMLCollection(TextCollection):

    def __init__(self, path="", indexer=None, preprocessor=None, use_parallel_computing=False):
        super().__init__(path, {}, use_parallel_computing)
        self.collection:list(XMLDocument) = []
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
        self.collection = self.preprocessor.pre_process(raw_collection, self.use_parallel_computing)
        self.Timer.stop()
        print(f"Collection of {len(self.collection)} documents, preprocessed in {self.Timer.get_time('preprocessing')} seconds.", file=stderr)

    def index(self) -> None:
        print("Indexing collection...", file=stderr)
        self.Timer.start("indexing")
        self.indexer.index(self.collection, self.use_parallel_computing)
        self.Timer.stop()
        print(f"Collection indexed in {self.Timer.get_time('indexing')} seconds.", file=stderr)
    
    def compute_stats(self) -> dict[int]:
         # Compute collection statistics
        print("Computing collection statistics...", file=stderr)
        self.Timer.start("compute_statistics")
        print("computing avdl ...", file=stderr)
        self.avdl = self._compute_avdl()
        print("computing avtl ...", file=stderr)
        self.avtl = self._compute_avtl()
        print("computing terms collection frequency ...", file=stderr)
        self.cf = self._compute_terms_collection_frequency()
        self.Timer.stop()
        print(f"Collection statistics computed in {self.Timer.get_time('compute_statistics')} seconds.", file=stderr)

    def _compute_avdl(self) -> float:
        return sum(len(d) for d in self.collection) / len(self.collection)
    
    def _compute_avtl(self) -> float:
        return sum(doc.compute_avtl() for doc in tqdm(self.collection, desc="Computing avtl ...")) / len(self.collection)
    
    def _compute_terms_collection_frequency(self) -> list[float]:
        return [self.indexer.get_df(term) for term in self.indexer.get_vocabulary()]

    def compute_RSV(self, query:str, type="xml") -> dict[str, float]:
        """
        compute the Relevant Status Value of a document for a query
        """
        if type == "xml":
            collection = copy.deepcopy(self.collection)
            for doc_xml in tqdm(self.collection, desc="Extracting XML elements from documents ...."):
                collection  += doc_xml.get_xml_element_list()
        else:
            collection = self.collection
        print(f"Computing RSV for {len(collection)} xpath...")
        scores = self.information_retriever.compute_scores(collection, query, self.indexer)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)
    

    def serialize(self, path:str) -> bool:
        try:
            c = copy.deepcopy(self)
            with open(path, 'wb') as f:
                pickle.dump(c, f)
            return True
        except Exception as e:
            print(f"Error serializing indexed collection to {path}: {e}", file=stderr)
            return False

    @classmethod
    def deserialize(cls, path:str) -> 'XMLCollection' :
        with open(path, 'rb') as f:
            index = pickle.Unpickler(f).load()

        if isinstance(index, cls):
            return index
        
        print(f"Deserialized object from {path} is not an instance of the Index class.", file=stderr)
        return None