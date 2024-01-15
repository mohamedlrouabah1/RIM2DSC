from __future__ import annotations
from models.concepts.InformationRessource import InformationRessource

class TextDocument(InformationRessource):
    """
    Represents a document and its related metadata.

    Attributes:
        - doc_id (int): Identifier for the document.
        - content (list[str]): List of content tokens in the document.

    Methods:
        __init__(doc_id: int, content: list[str]): Initializes the TextDocument object.
        get_next_token() -> str: Generator function to yield the next token in the document.
        compute_avtl() -> float: Computes the average term length in the document.
    """

    def __init__(self, doc_id:int, content:list[str]):
        """
        Initializes the TextDocument object.

        Params:
        -------
        doc_id: int
            Identifier for the document.
        content: list[str]
            List of content tokens in the document.
        """
        super().__init__(doc_id, content)

    def get_next_token(self) -> str:
        """
        Generator function to yield the next token in the document.
        """
        for token in self.content:
            yield token

    def compute_avtl(self) -> float:
        return sum(len(t) for t in self.content) / len(self.content)
