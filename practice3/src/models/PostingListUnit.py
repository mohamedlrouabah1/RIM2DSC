class PostingListUnit:
    """
    Define what a posing list cell stored.
    """
    def __init__(self, document_id:int, frequency:int):
        self.document_id = document_id
        self.frequency = frequency
