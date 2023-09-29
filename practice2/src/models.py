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

    def add_document(self, document:Document):
        self.documents.append(document)

class PostingListUnit:
    def __init__(self, document_id:int, frequency:int):
        self.document_id = document_id
        self.frequency = frequency

class PostingList:
    def __init__(self, term:str):
        self.term = term
        self.postings: dict(PostingListUnit) = {}
        self.document_frequency = 0
        self.total_frequency = 0

    def add_posting(self, posting:PostingListUnit):
        self.postings[posting.document_id] =posting
        self.document_frequency += 1
        self.total_frequency += posting.frequency

class Index:
    def __init__(self):
        self.posting_lists: list(PostingList) = {}
        self.collection = Collection()
        self.indexing_time_in_ns = -1.0

    def get_vocabulary_size(self):
        return len(self.posting_lists)
    
    def get_vocabulary(self):
        return self.posting_lists.keys()
    
    def get_term_frequency(self, term:str):
        return self.posting_lists[term].total_frequency

    def __str__(self):
        return f"Index with {self.get_vocabulary_size()} terms"