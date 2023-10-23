from models.PostingListUnit import PostingListUnit

class PostingList:
    """ 
    Store the posting list of a term and its related metadata.
    """
    def __init__(self, term:str):
        self.term = term
        self.postings: dict(PostingListUnit) = {}
        self.document_frequency = 0
        self.total_frequency = 0

    def add_posting(self, posting:PostingListUnit):
        self.postings[posting.document_id] =posting
        self.document_frequency += 1
        self.total_frequency += posting.frequency