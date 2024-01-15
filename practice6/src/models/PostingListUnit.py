from __future__ import annotations

class PostingListUnit:
    """
    PostingListUnit class represents a unit of information within a posting list.

    Attributes:
    -----------
    - document_id: int
        The ID of the document where the term appears.
    - frequency: float
        The frequency of the term in the document.

    Methods:
    --------
    - __init__(self, document_id:int, frequency:float):
        Constructor for PostingListUnit.
    - __str__(self) -> str:
        String representation of the PostingListUnit object.

    """

    def __init__(self, document_id:int, frequency:float):
        """
        Constructor for PostingListUnit.

        Params:
        -------
        - document_id: int
            The ID of the document where the term appears.
        - frequency: float
            The frequency of the term in the document.
        """
        self.document_id = document_id
        self.frequency = frequency

    def __str__(self) -> str:
        return f"Document ID: {self.document_id} - Frequency: {self.frequency}"
