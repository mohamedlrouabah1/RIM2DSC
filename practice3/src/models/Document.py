class Document:
    """
    Store a document and its related metadata.
    """
    def __init__(self, id:int, content:str):
        self.id = id
        self.content = content
        self.length = len(content)