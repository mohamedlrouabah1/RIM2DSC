class Document:
    """
    Store a document and its related metadata.
    """
    # def __init__(self, id:int, content, tag_id, tag_path=""):
    #     self.id = id
    #     self.content = content
    #     self.tag_id = tag_id
    #     self.tag_path = tag_path
    
    def __init__(self, id:int, metadata):
        self.id = id
        self.metadata = metadata

    def __len__(self):
        return sum(len(metadata[-1]) for metadata in self.metadata)

    def __repr__(self):
        return f"Document(id={self.id}, metadata={self.metadata})"

    def __str__(self):
        return f"Document {self.id} ({len(self)} tokens)"

    def get_next_token(self):
        for metadata in self.metadata:
            for token in metadata[-1]:
                yield token

    def get_tokens(self):
        return [token for metadata in self.metadata for token in metadata[-1]]

    def compute_avtl(self):
        total_tokens = sum(len(metadata[-1]) for metadata in self.metadata)
        return total_tokens / len(self.metadata) if len(self.metadata) > 0 else 0

    def get_tag_paths(self):
        return [metadata[1] for metadata in self.metadata]

    
    # def to_dict(self):
    #     return {'id': self.id, 'metadata': {'tag_id': self.tag_id, 'tag_path': self.tag_path, 'content': self.content}}
