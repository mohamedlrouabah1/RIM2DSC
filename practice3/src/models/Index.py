from models.Collection import Collection
from models.PostingList import PostingList

class Index:
    def __init__(self):
        self.posting_lists: list(PostingList) = {}
        self.collection = Collection()
        self.indexing_time_in_ns = -1.0
        self.preprocessing_time_in_ns = -1.0 

    def get_vocabulary_size(self):
        return len(self.posting_lists)
    
    def get_vocabulary(self):
        return self.posting_lists.keys()
    
    def get_term_frequency(self, term:str):
        return self.posting_lists[term].total_frequency

    def __str__(self):
        return f"Index with {self.get_vocabulary_size()} terms"