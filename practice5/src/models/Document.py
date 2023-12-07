class Document:
    """
    Store a document and its related metadata.
    """
    # def __init__(self, id:int, content, tag_id, tag_path=""):
    #     self.id = id
    #     self.content = content
    #     self.tag_id = tag_id
    #     self.tag_path = tag_path
    
    def __init__(self, id, tag_id_counter, xpath, content):
        self.id = id
        self.tag_id_counter = tag_id_counter
        self.xpath = xpath
        self.content = content

    def __len__(self):
        return len(self.content)
    
    def __str__(self) -> str:
        return f"Document {self.id} ({len(self.content)} tokens)"

    def get_next_token(self):
        for token in self.content:
            yield token

    def get_tokens(self):
        return self.content

    def compute_avtl(self):
        return sum(len(t) for t in self.content) / len(self.content)

    def get_tag_path(self):
        return self.xpath

    def get_xpath_ids(self):
        return f"{self.id}:{self.xpath}"
    # def to_dict(self):
    #     return {'id': self.id, 'metadata': {'tag_id': self.tag_id, 'tag_path': self.tag_path, 'content': self.content}}
