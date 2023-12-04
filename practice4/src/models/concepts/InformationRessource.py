from abc import ABC

class InformationRessource(ABC):
    """
    Represent an information ressources in the context of information retrieval.

    Attributes:
        - id: int, The id of the ressource.
        - content: Any, The content of the ressource.
    """

    def __init__(self, id:int, content:any):
        self.id, self.content= id, content
    
    def __repr__(self) -> str:
        s = ">"*50 + "\n"
        s += f"Document {self.id}\n"
        s += self.content.__repr__()
        s += "<"*50 + "\n"

    def get_id(self) -> int:
        return self.id

    def get_content(self) -> any:
        return self.content