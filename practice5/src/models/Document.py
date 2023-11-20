class Document:
    """
    Store a document and its related metadata.
    """
    def __init__(self, id:int, content, granularity_info=None, tag_path="", original_tag_path=""):
        self.id = id
        self.content = content
        self.granularity_info = granularity_info
        self.tag_path = tag_path
        self.original_tag_path = original_tag_path
    def __len__(self):
        return len(self.content)
    
    def __repr__(self) -> str:
        pass

    def __str__(self) -> str:
        return f"Document {self.id} ({len(self.content)} tokens)"

    def get_next_token(self) -> str:
        for token in self.content:
            yield token

    def get_tokens(self):
        return self.content
                
    def compute_avtl(self):
    # a retravailler pour que utilise la nouvelle taille de tous les xml parser et integere pas encore fait
        if not self.content:
            return 0
        return sum(len(t) for t in self.content) / len(self.content)