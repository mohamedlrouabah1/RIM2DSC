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
        id = posting.document_id.split(':')[0]
        if id not in self.doc_ids:
            self.doc_ids.add(id)
            self.document_frequency += 1
            self.total_frequency += posting.frequency

        self.postings[posting.document_id] = posting

    def get_tfd(self, doc_id:int):
        if self.postings.get(doc_id) is None:
            return 0
        return self.postings[doc_id].frequency
