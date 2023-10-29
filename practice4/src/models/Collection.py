import gzip
from tqdm import tqdm
from models.Document import Document
from models.Timer import Timer
from models.TextPreprocessor import TextPreprocessor
from models.Indexer import Indexer
from models.weighting.BM25 import BM25

# TODO make a subclass Collection Inex
# to make specific function to extract documents
# from loaded files
class Collection:
    """"
    Store a collection of documents and its related metadata.
    """
    def __init__(self, path, indexer=None, preprocessor=None, ranking_function=None):
        self.documents:list(Document) = []
        self.terms_frequency:dict(str, int) = {}
        self.vocabulary_size = 0
        self.path = path
        self.Timer = Timer()
        self.preprocessor = TextPreprocessor() if preprocessor is None else preprocessor
        self.indexer = Indexer() if indexer is None else indexer
        self.information_retriever = BM25() if ranking_function is None else ranking_function


    def load_and_preprocess(self):
        print("Loading collection from file {path} ...")
        self.Timer.start("load_collection")
        collection_string = self.preprocessor.load_and_lower_text_collection(self.path)
        self.Timer.stop("load_collection")
        print(f"Collection loaded in {self.Timer.get_time('load_collection')} seconds.")

        print("Preprocessing collection...")
        self.Timer.start("preprocessing")
        doc_token_list = self.preprocessor.pre_process(collection_string)
        self.Timer.stop("preprocessing")
        print(f"Collection preprocessed in {self.Timer.get_time('preprocessing')} seconds.")

        print("Instantiate Document objects...")
        self.Timer.start("instantiate_documents")
        self.documents = [ Document(doc_id, doc_tokens) 
                          for doc_id, doc_tokens in 
                          tqdm(doc_token_list, desc="Instantiating documents...", colour="blue")
                          ]
        self.Timer.stop("instantiate_documents")
        print(f"Documents instantiated in {self.Timer.get_time('instantiate_documents')} seconds.")


    def compute_index(self, save=True):
        print("Indexing collection...")
        self.Timer.start("indexing")
        map(self.indexer.index_doc, self.documents)
        self.Timer.stop("indexing")
        print(f"Collection indexed in {self.Timer.get_time('indexing')} seconds.")

        # print("Save index to disk...")
        # path = "index.pkl"


    def load_collection(self, path):
        # Compute collection statistics
        print("Computing collection statistics...")
        self.Timer.start("compute_statistics")
        self.avdl = self.compute_avdl()
        self.avtl = self.compute_avtl()
        self.cf = self.compute_terms_collection_frequency()
        self.Timer.stop("compute_statistics")
        print(f"Collection statistics computed in {self.Timer.get_time('compute_statistics')} seconds.")



    def __len__(self):
        return len(self.documents)

    def compute_avdl(self):
        return sum(len(d) for d in self.documents) / len(self.documents)
    
    def get_avdl(self):
        return self.avdl
    
    def compute_avtl(self):
        return sum(doc.compute_avtl() for doc in self.documents) / len(self.documents)
    
    def get_avtl(self):
        return self.avtl

    def get_vocabulary_size(self):
        return len(self.indexer)
    
    def compute_terms_collection_frequency(self):
        return [self.indexer.get_term_frequency(term) for term in self.indexer.get_vocabulary()]
    
    def get_cf(self, term:str):
        return self.indexer.get_term_frequency(term)
    
    def get_terms_collection_frequency(self):
        return self.cf
    
    def __str__(self) -> str:
        s = "-"*50 + "\n"
        s += f"Collection: {self.path}\n"
        s += f"Number of documents: {len(self.documents)}\n"
        s += f"Average Document Length: {self.avdl} (words)\n"
        s += f"Average Term Length: {self.avtl} (characters)\n"
        s += f"Vocabulary Size: {self.get_vocabulary_size()} (unique terms)\n"
        s += f"Total Collection Frequency: {sum(self.cf)} (terms)\n"
        s += f"Loading time: {self.Timer.get_time('load_collection')} seconds\n"
        s += f"Preprocessing time: {self.Timer.get_time('preprocessing')} seconds\n"
        s += f"Indexation time: {self.Timer.get_time('indexing')} seconds\n"
        s += f"Total time: {self.Timer.get_time('preprocessing') + self.Timer.get_time('indexing')} seconds\n"
        s += f"Computing statistics time: {self.Timer.get_time('compute_statistics')} seconds\n"
        s += "-"*50 + "\n"

    def __repr__(self) -> str:
        pass
