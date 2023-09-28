"""
Define the classes for the indexing of the documents.
"""
class Document:
    def __init__(self, id:int, content:str):
        self.id = id
        self.content = content
        self.lenth = len(content)

class Collection:
    def __init__(self):
        self.documents:list(Document) = []
        self.terms_frequency:dict(str, int) = {}
        self.vocabulary_size = 0

class PostingListUnit:
    def __init__(self, document_id:int, frequency:int):
        self.document_id = document_id
        self.frequency = frequency

class PostingList:
    def __init__(self, term:str):
        self.term = term
        self.postings = []
        self.document_frequency = 0
        self.total_frequency = 0

    def add_posting(self, posting:PostingListUnit):
        self.postings.append(posting)
        self.document_frequency += 1
        self.total_frequency += posting.frequency

class Index:
    def __init__(self):
        self.posting_lists = {}
        self.collection = Collection()

    def get_vocabulary_size(self):
        return len(self.posting_lists)
    
    def get_vocabulary(self):
        return self.posting_lists.keys()
    
    def get_term_frequency(self, term:str):
        return self.posting_lists[term].total_frequency