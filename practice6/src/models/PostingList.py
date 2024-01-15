from __future__ import annotations
from models.PostingListUnit import PostingListUnit

class PostingList:
    """
    PostingList class represents a posting list for a specific term in an
    information retrieval system.

    Attributes:
    -----------
    - term: str
        The term for which the posting list is created.
    - postings: dict(PostingListUnit)
        Dictionary storing PostingListUnit objects for different documents.
    - document_frequency: int
        The number of documents in which the term appears.
    - total_frequency: int
        The total frequency of the term across all documents.
    - doc_ids: set
        Set storing unique document IDs in which the term appears.

    Methods:
    --------
    - __init__(self, term:str):
        Constructor for PostingList.
    - __len__(self):
        Get the document frequency of the term.
    - __str__(self) -> str:
        String representation of the PostingList object.
    - add_posting(self, posting:PostingListUnit):
        Add a PostingListUnit to the posting list.
    - get_tfd(self, doc_id:int) -> int:
        Get the term frequency in a specific document.

    """

    def __init__(self, term:str):
        """
        Constructor for PostingList.

        Params:
        -------
        - term: str
            The term for which the posting list is created.
        """
        self.term = term
        self.postings: dict(PostingListUnit) = {}
        self.document_frequency = 0
        self.total_frequency = 0
        self.doc_ids = set()

    def __len__(self):
        return self.document_frequency

    def __str__(self) -> str:
        s = f"""
        {'+'*50}\n
        Term: {self.term}\n
        Number of documents: {self.document_frequency}\n
        Total frequency: {self.total_frequency}\n
        """
        for xpath, value in self.postings.items():
            s += f"PostingListUnit {xpath} : {value.__str__()}\n"
        s += f"{'+'*50}\n"

        return s

    def add_posting(self, posting:PostingListUnit):
        # If it is the first time we index an xml element of this document, we add it to the list
        doc_id = posting.document_id.split(':')[0]
        if doc_id not in self.doc_ids:
            self.doc_ids.add(doc_id)
            self.document_frequency += 1
            self.total_frequency += posting.frequency

        self.postings[posting.document_id] = posting

    def get_tfd(self, doc_id:int):
        if self.postings.get(doc_id) is None:
            return 0
        return self.postings[doc_id].frequency
