import gzip
from models.Document import Document

# TODO make a subclass Collection Inex
# to make specific function to extract documents
# from loaded files
class Collection:
    """"
    Store a collection of documents and its related metadata.
    """
    def __init__(self, path):
        self.documents:list(Document) = []
        self.terms_frequency:dict(str, int) = {}
        self.vocabulary_size = 0
        self.path = path
        self.docs_string = self.load_collection(path)
        # TODO: create Document from this string
        # and store the preprocess version of them.


    def __len__(self):
        return len(self.documents)

    def add_document(self, document:Document):
        self.documents.append(document)

    def load_text_collection(self, path) -> str:
        """
        Read the document collection from a file.
        Handles both regular and gzipped files.

        Returns:
            str: the document collection as a lowered 
                 string
        """
        with open(path, 'r') as f:
            document_collection_str = f.read().lower()
        return document_collection_str

