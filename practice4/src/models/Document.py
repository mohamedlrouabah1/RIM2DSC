class Document:
    """
    Store a document and its related metadata.
    """
    def __init__(self, id:int, content:str):
        self.id = id
        self.content = content
        self.length = len(content)

    def __len__(self):
        return self.length
    
    def __str__(self) -> str:
        # TODO: return a string representation of the document
        # its metadata.
        pass