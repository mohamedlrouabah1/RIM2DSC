from models.Collection import Collection
from models.PostingList import PostingList

class Index:
    def __init__(self, collection:Collection=None):
        self.posting_lists: list(PostingList) = {}
        self.collection = Collection() if collection is None else collection
        self.indexing_time_in_ns = -1.0
        self.preprocessing_time_in_ns = -1.0 

    def get_vocabulary_size(self):
        return len(self.posting_lists)
    
    def get_vocabulary(self):
        return self.posting_lists.keys()
    
    def get_term_frequency(self, term:str):
        return self.posting_lists[term].total_frequency

    def __str__(self):
        s = "-"*50 + "\n"
        s += f"Indexing the collection at {self.collection.path}" + "\n"
        s += f"Preprocessing time: {self.preprocessing_time_in_ns} ns" + "\n"
        s += f"Indexing time: {self.indexing_time_in_ns} ns" + "\n"
        s += f"Vocabulary size: {self.get_vocabulary_size()}" + "\n"

        # print(f"Average Document Length: {avg_doc_len} (words)")
        # print(f"Average Term Length: {avg_term_len} (characters)")
        # print(f"Vocabulary Size: {vocab_size} (unique terms)")
        # print(f"Total Collection Frequency: {total_coll_freq} (terms)")
        # print("Indexation time: ")
        # print_time(chartname,index.indexing_time_in_ns)
        # print("Preprocessing time: ")
        # print_time(chartname,index.preprocessing_time_in_ns)

        s = "-"*50 + "\n"
        
        return s