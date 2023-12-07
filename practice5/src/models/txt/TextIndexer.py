import os
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from models.Document import Document
from models.PostingList import PostingList
from models.PostingListUnit import PostingListUnit

class TextIndexer:

    def __init__(self,):
        self.posting_lists: dict(PostingList) = {}

    def __len__(self) -> int:
        return len(self.posting_lists)

    @DeprecationWarning
    def __str__(self) -> str:
        """Deprecated. Use Collection__str__ instead. Will be updated later."""
        return f"""
        {'-'*50}\n
        Indexing the collection at {self.collection.path}\n"
        Preprocessing time: {self.preprocessing_time_in_ns} ns\n
        Indexing time: {self.indexing_time_in_ns} ns\n
        Vocabulary size: {self.get_vocabulary_size()}\n
        Vocabulary Size: {self.get_vocabulary_size} (unique terms)\n
        Indexation time: {self.indexing_time_in_ns} ns\n
        Preprocessing time: {self.preprocessing_time_in_ns} ns\n
        {'-'*50}\n
        """
    
    def get_vocabulary_size(self) -> int:
        return len(self.posting_lists)
    
    def get_vocabulary(self) -> list(str):
        return self.posting_lists.keys()
    
    def get_df(self, term:str) -> int:
        """ Return the number of documents in which the term appears."""
        if self.posting_lists.get(term) is None:
            return 0  
        return len(self.posting_lists[term])
    
    def get_tf(self, term:str, doc_id:int) -> int:
        """ Return the term frequency of the term in the document."""
        if self.posting_lists.get(term) is None:
            return 0
        return self.posting_lists[term].get_tfd(doc_id)    

    def _index_doc(self, doc:Document) -> None:
        """
        Create the posting lists for the given document.
        """
        tokens = doc.get_tokens()
        id = doc.id
        tf = Counter(tokens)
        
        for term, freq in tf.items():
            unit = PostingListUnit(id, freq)

            if self.posting_lists.get(term) is None:
                self.posting_lists[term] = PostingList(term)
            else:
                self.posting_lists[term].add_posting(unit)
        return

    def index(self, docs:list(Document), use_parallel_computing=False) -> None:
        if not use_parallel_computing:
            for doc in docs: self._index_doc(doc)
            return
        
        print("Using pool to index documents.")
        num_processes = os.cpu_count()
        indexing = lambda doc : self._index_doc(doc)

        with ProcessPoolExecutor(num_processes) as executor:
            results = executor.map(indexing, docs)
