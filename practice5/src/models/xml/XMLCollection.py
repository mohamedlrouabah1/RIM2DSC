import xml.dom.minidom as minidom
import pickle
#import hickle as hkl

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


    def compute_RSV(self, query:str, type="xml") -> dict[str, float]:
        """
        compute the Relevant Status Value of a document for a query
        Return the result sorted by doc id then score, in reverse order)
        """
        if type == "xml":
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
