import pickle
from collections import Counter
from models.Document import Document
from models.PostingList import PostingList
from models.PostingListUnit import PostingListUnit

class Indexer:
    def __init__(self,):
        self.posting_lists: list(PostingList) = {}

    def get_vocabulary_size(self):
        return len(self.posting_lists)
    
    def get_vocabulary(self):
        return self.posting_lists.keys()
    
    def get_term_frequency(self, term:str):
        return self.posting_lists[term].total_frequency
    
    def serialize(self, path) -> bool:
        try:
            with open(path, 'wb') as f:
                pickle.dump(self, f)
            return True
        except Exception as e:
            print(f"Error serializing index to {path}: {e}")
            return False

    @classmethod
    def deserialize(cls, path):
        with open(path, 'rb') as f:
            index = pickle.load(f)

        if isinstance(index, cls):
            return index
        
        print(f"Deserialized object from {path} is not an instance of the Index class.")
        return None


    def __str__(self):
        s = "-"*50 + "\n"
        #s += f"Indexing the collection at {self.collection.path}" + "\n"
        s += f"Preprocessing time: {self.preprocessing_time_in_ns} ns" + "\n"
        s += f"Indexing time: {self.indexing_time_in_ns} ns" + "\n"
        s += f"Vocabulary size: {self.get_vocabulary_size()}" + "\n"

        # print(f"Average Document Length: {avg_doc_len} (words)")
        # print(f"Average Term Length: {avg_term_len} (characters)")
        s += f"Vocabulary Size: {self.get_vocabulary_size} (unique terms)" + "\n"
        # print(f"Total Collection Frequency: {total_coll_freq} (terms)")
        s =+ f"Indexation time: {self.indexing_time_in_ns} ns" + "\n"
        s += f"Preprocessing time: {self.preprocessing_time_in_ns} ns" + "\n"

        s = "-"*50 + "\n"
        
        return s
    

    def index_doc(self, doc:Document) -> None:
        """
        Create the posting lists for the given document.
        """
        tokens = doc.get_tokens()
        id = doc.get_id()
        tf = Counter(tokens)
        
        for term, freq in tf.items():
            unit = PostingListUnit(id, freq)

            if self.posting_lists.get(term) is None:
                self.posting_lists[term] = PostingList(term)
            else:
                self.posting_lists[term].add_posting(unit)

    def __len__(self):
        return len(self.posting_lists)