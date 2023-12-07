import matplotlib.pyplot as plt
import os
import pickle
from tqdm import tqdm

from models.concepts.CollectionOfRessources import CollectionOfRessources
from models.Document import Document
from models.Indexer import Indexer
from models.TextPreprocessor import TextPreprocessor
from models.Timer import Timer
from models.weighting.WeightingFunction import WeightingFunction
from utilities.config import GRAPH_FOLDER


class TextCollection(CollectionOfRessources):
    """"
    Store a collection of documents and its related metadata.
    """
    def __init__(self, path="", indexer=None, preprocessor=None, use_parallel_computing=False):
        super().__init__(path, {})
        self.documents:list(Document) = []
        self.terms_frequency:dict(str, int) = {}
        self.vocabulary_size = 0
        self.path = path
        self.Timer = Timer()
        self.preprocessor = TextPreprocessor() if preprocessor is None else preprocessor
        self.indexer = Indexer() if indexer is None else indexer
        self.information_retriever = None
        self.use_parallel_computing = use_parallel_computing
   
    def __str__(self) -> str:
        return f"""
         {'-'*50}\n
        Collection: {self.path}\n
        Number of documents: {len(self.documents)}\n
        Average Document Length: {self.avdl} (words)\n
        Average Term Length: {self.avtl} (characters)\n
        Vocabulary Size: {self.get_vocabulary_size()} (unique terms)\n
        Total Collection Frequency: {sum(self.cf)} (terms)\n
        Loading time: {self.Timer.get_time('load_collection')} seconds\n
        Preprocessing time: {self.Timer.get_time('preprocessing')} seconds\n
        Indexation time: {self.Timer.get_time('indexing')} seconds\n
        Total time: {self.Timer.get_time('preprocessing') + self.Timer.get_time('indexing')} seconds\n
        Computing statistics time: {self.Timer.get_time('compute_statistics')} seconds\n
        {'-'}*50\n
        """
    
    def set_ranking_function(self, ranking_function:WeightingFunction) -> None:
        self.information_retriever = ranking_function
    
    def get_avdl(self) -> float:
        return self.avdl
    
    def get_avtl(self) -> float:
        return self.avtl

    def get_vocabulary_size(self) -> int:
        return len(self.indexer)    
    
    def get_terms_collection_frequency(self) -> float:
        return self.cf

    def load(self) -> str:
        print(f"Loading collection from file {self.path} ...")
        self.Timer.start("load_collection")
        collection_string = self.preprocessor.load_and_lower_text_collection(self.path)
        self.Timer.stop()
        print(f"Collection loaded in {self.Timer.get_time('load_collection')} seconds.")
        return collection_string

    def preprocess(self, raw_collection) -> None:
        print("Preprocessing collection...")
        self.Timer.start("preprocessing")
        doc_token_list = self.preprocessor.pre_process(raw_collection, self.use_parallel_computing)
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


    def index(self) -> None:
        print("Indexing collection...")
        self.Timer.start("indexing")
        self.indexer.index(self.documents, self.use_parallel_computing)
        self.Timer.stop()
        print(f"Collection indexed in {self.Timer.get_time('indexing')} seconds.")

    def compute_RSV(self, query:str) -> dict(str, float):
        """
        compute the Relevant Status Value of a document for a query
        """
        scores = self.information_retriever.compute_scores(self.documents, query, self.indexer)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def compute_stats(self) -> None:
        # Compute collection statistics
        print("Computing collection statistics...")
        self.Timer.start("compute_statistics")
        self.avdl = self._compute_avdl()
        self.avtl = self._compute_avtl()
        self.cf = self._compute_terms_collection_frequency()
        self.Timer.stop()
        print(f"Collection statistics computed in {self.Timer.get_time('compute_statistics')} seconds.")

    def plot_stats(self) -> None: 
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

    def _compute_avdl(self) -> float:
        return sum(len(d) for d in self.documents) / len(self.documents)
    
    def _compute_avtl(self) -> float:
        return sum(doc.compute_avtl() for doc in self.documents) / len(self.documents)
    
    def _compute_terms_collection_frequency(self) -> list(float):
        return [self.indexer.get_df(term) for term in self.indexer.get_vocabulary()]
     
    def __reduce__(self) -> tuple:
        # Exclude the 'doc_preprocessing' and 'pre_process' methods from pickling
        state = self.__dict__.copy()
        state.pop('preprocessor', None)
        return (self.__class__, (), state)
    
    def serialize(self, path:str) -> bool:
        try:
            with open(path, 'wb') as f:
                pickle.dump(self, f)
            return True
        except Exception as e:
            print(f"Error serializing indexed collection to {path}: {e}")
            return False

    @classmethod
    def deserialize(cls, path:str) -> 'TextCollection' :
        with open(path, 'rb') as f:
            index = pickle.load(f)

        if isinstance(index, cls):
            return index
        
        print(f"Deserialized object from {path} is not an instance of the Index class.")
        return None
