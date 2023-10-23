from models.Document import Document

class Collection:
    """"
    Store a collection of documents and its related metadata.
    """
    def __init__(self):
        self.documents:list(Document) = []
        self.terms_frequency:dict(str, int) = {}
        self.vocabulary_size = 0

    def add_document(self, document:Document):
        self.documents.append(document)