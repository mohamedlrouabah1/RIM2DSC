from abc import ABC
from typing import Any

class InformationRessource(ABC):
    """
    Represent an information ressources in the context of information retrieval.

    Attributes:
        - id: int, The id of the ressource.
        - content: Any, The content of the ressource.
    """

    def __init__(self, id:int, content:Any):
        self.id, self.content= id, content

    def __len__(self) -> int:
        return len(self.content)
    
    def __str__(self) -> str:
        return f"Document {self.id} ({len(self.content)} pieces of information."
    
    def __repr__(self) -> str:
        s = ">"*50 + "\n"
        s += f"Document {self.id}\n"
        s += self.content.__repr__()
        s += "<"*50 + "\n"

    def get_id(self) -> int:
        return self.id

    def get_content(self) -> Any:
        return self.content