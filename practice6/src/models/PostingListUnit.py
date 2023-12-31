class PostingListUnit:
    """
    Define what a posing list cell stored.
    """
    def __init__(self, document_id:int, frequency:float):
        self.document_id = document_id
        self.frequency = frequency
    
    def __str__(self) -> str:
        return f"Document ID: {self.document_id} - Frequency: {self.frequency}"