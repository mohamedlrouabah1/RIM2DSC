from typing import List
from models.concepts.InformationRessource import InformationRessource

class TextDocument(InformationRessource):
    """
    Store a document and its related metadata.
    """
    def __init__(self, id:int, content:List[str]):
        super().__init__(id, content)

    def get_next_token(self) -> str:
        for token in self.content:
            yield token

    def compute_avtl(self) -> float:
        return sum(len(t) for t in self.content) / len(self.content)
