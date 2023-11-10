import gzip
import matplotlib.pyplot as plt
import os
import pickle
from tqdm import tqdm
from models.Document import Document
from models.Timer import Timer
from models.TextPreprocessor import TextPreprocessor
from models.Indexer import Indexer
from models.weighting.BM25 import BM25
from utilities.config import GRAPH_FOLDER

# TODO make a subclass Collection Inex
# to make specific function to extract documents
# from loaded files
class Collection:
    """"
    Store a collection of documents and its related metadata.
    """
    def __init__(self, path="", indexer=None, preprocessor=None, use_parallel_computing=False):
        self.documents:list(Document) = []
        self.terms_frequency:dict(str, int) = {}
        self.vocabulary_size = 0
        self.path = path
        self.Timer = Timer()
        self.preprocessor = TextPreprocessor() if preprocessor is None else preprocessor
        self.indexer = Indexer() if indexer is None else indexer
        self.information_retriever = None
        self.use_parallel_computing = use_parallel_computing


    def load_and_preprocess(self):
        print("Loading collection from file {path} ...")
        self.Timer.start("load_collection")
        collection_string = self.preprocessor.load_and_lower_text_collection(self.path)
        self.Timer.stop()
        print(f"Collection loaded in {self.Timer.get_time('load_collection')} seconds.")

        print("Preprocessing collection...")
        self.Timer.start("preprocessing")
        doc_token_list = self.preprocessor.pre_process(collection_string, self.use_parallel_computing)
        self.Timer.stop()
        print(f"Collection preprocessed in {self.Timer.get_time('preprocessing')} seconds.")

        print("Instantiate Document objects...")
        self.Timer.start("instantiate_documents")
        self.documents = [ Document(doc_id, doc_tokens) 
                          for doc_id, doc_tokens in 
                          tqdm(doc_token_list, desc="Instantiating documents...", colour="blue")
                          ]
        self.Timer.stop()
        print(f"Documents instantiated in {self.Timer.get_time('instantiate_documents')} seconds.")


    def compute_index(self, save=True):
        print("Indexing collection...")
        self.Timer.start("indexing")
        self.indexer.index(self.documents, self.use_parallel_computing)
        self.Timer.stop()
        print(f"Collection indexed in {self.Timer.get_time('indexing')} seconds.")

        # print("Save index to disk...")
        # path = "index.pkl"


    def compute_statistics(self):
        # Compute collection statistics
        print("Computing collection statistics...")
        self.Timer.start("compute_statistics")
        self.avdl = self.compute_avdl()
        self.avtl = self.compute_avtl()
        self.cf = self.compute_terms_collection_frequency()
        self.Timer.stop()
        print(f"Collection statistics computed in {self.Timer.get_time('compute_statistics')} seconds.")



    def __len__(self):
        """ Return the number of documents in the collection """
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
        return [self.indexer.get_df(term) for term in self.indexer.get_vocabulary()]
    
    
    def get_terms_collection_frequency(self):
        return self.cf
    
    def set_ranking_function(self, ranking_function):
        self.information_retriever = ranking_function

    def search(self, query, k=10):
        return self.information_retriever.search(query, k)
    
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
        return s

    def __repr__(self) -> str:
        pass


    def plot_statistics(self): 
        labels = ["Avg Doc Length", "Avg Term Length", "Vocabulary Size", "Total Collection Frequency", "Preprocessing Time (seconds)", "Indexing Time (seconds)"]
        values = [self.avdl, self.avtl, self.get_vocabulary_size(), sum(self.cf), self.Timer.get_time('preprocessing') + self.Timer.get_time('indexing')]

        plt.figure(figsize=(12, 8))
        bars = plt.bar(labels, values, color=['blue', 'green', 'red', 'purple', 'cyan'])
        
        # Use logarithmic scale for y-axis
        plt.yscale('log')
        plt.ylabel('Value (log scale)')
        plt.title(f'Metrics for the Collection: {self.path}')
        # Define units or descriptors
        units = ["(words)", "(characters)", "(unique terms)", "(terms)", "(seconds)"]

        # Annotate with exact values and units
        for i, bar in enumerate(bars):
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + (0.02 * yval), f"{round(yval, 2)} {units[i]}", ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        plt.savefig(os.path.join(GRAPH_FOLDER, f"{self.path}_Metrics_Bar_Plot.png"))
        plt.show()


    def RSV(self, query):
        """
        compute the Relevant Status Value of a document for a query
        """
        scores = self.information_retriever.compute_scores(self.documents, query, self.indexer)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)
    

    def __reduce__(self):
        # Exclude the 'doc_preprocessing' and 'pre_process' methods from pickling
        state = self.__dict__.copy()
        state.pop('preprocessor', None)
        return (self.__class__, (), state)
    

    def serialize(self, path) -> bool:
        try:
            with open(path, 'wb') as f:
                pickle.dump(self, f)
            return True
        except Exception as e:
            print(f"Error serializing indexed collection to {path}: {e}")
            return False

    @classmethod
    def deserialize(cls, path):
        with open(path, 'rb') as f:
            index = pickle.load(f)

        if isinstance(index, cls):
            return index
        
        print(f"Deserialized object from {path} is not an instance of the Index class.")
        return None
    
    def set_ranking_function(self, ranking_function):
        self.information_retriever = ranking_function