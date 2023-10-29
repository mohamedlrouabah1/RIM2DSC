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
    
    def get_df(self, term:str):
        """
        Return the number of documents in which the term appears.
        """
        return len(self.posting_lists[term])
    
    def get_term_frequency_document(self, term:str, doc_id:int):
        return self.posting_lists[term].get_tfd(doc_id)
    

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