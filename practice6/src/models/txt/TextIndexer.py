from __future__ import annotations
import os
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

from models.concepts.InformationRessource import InformationRessource
from models.txt.TextDocument import TextDocument
from models.PostingList import PostingList
from models.PostingListUnit import PostingListUnit

class TextIndexer:
    """
    Indexer for creating posting lists based on the input documents.

    Attributes:
        - posting_lists (dict[PostingList]): Dictionary storing posting lists for each term.

    Methods:
        __init__(): Initializes the TextIndexer object.
        __len__() -> int: Returns the number of terms in the vocabulary.
        __str__() -> str: Returns a string representation of the object.
        get_vocabulary_size() -> int: Returns the size of the vocabulary.
        get_vocabulary() -> list[str]: Returns a list of terms in the vocabulary.
        get_df(term: str) -> int: Returns the document frequency of a term.
        get_tf(term: str, doc_id: int) -> int: Returns the term frequency in a document.
        _index_text(doc: InformationRessource, content=None) -> None: Creates posting lists for a document.
        index(docs: list[TextDocument], use_parallel_computing=False) -> None: Indexes documents.

    """

    def __init__(self):
       self.posting_lists: dict[PostingList] = {}

    def __len__(self):
        return len(self.posting_lists)

    def __str__(self) -> str:
        s = f"""
        {'-'*50}\n
        Number of terms: {self.__len__()}\n
        Posting lists:\n
        """
        i=0
        for key, value in self.posting_lists.items():
            s += f"posting list {key} : {value.__str__()}\n"
            i+=1
            if i > 50:
                break
        s+= f"{'-'*50}\n"
        return s

    def get_vocabulary_size(self) -> int:
        return len(self.posting_lists)

    def get_vocabulary(self) -> list[str]:
        return self.posting_lists.keys()

    def get_df(self, term:str) -> int:
        """ Return the number of documents in which the term appears."""
        if term not in self.posting_lists:
            return 0

        return len(self.posting_lists[term])

    def get_tf(self, term:str, doc_id:int) -> int:
        """ Return the term frequency of the term in the document."""
        if self.posting_lists.get(term) is None:
            return 0
        return self.posting_lists[term].get_tfd(doc_id)

    def _index_text(self, doc:InformationRessource, content=None) -> None:
        """
        Create the posting lists for the given document.
        """
        tokens = doc.content if content is None else content
        doc_id = doc.id
        tf = Counter(tokens)
        for term, freq in tf.items():
            unit = PostingListUnit(doc_id, freq)

            if not (term in self.posting_lists):
                self.posting_lists[term] = PostingList(term)

            self.posting_lists[term].add_posting(unit)

    def index(self, docs:list[TextDocument], use_parallel_computing=False) -> None:
        """
        Indexes documents.

        Params:
        -------
        docs: list[TextDocument]
            List of TextDocument objects.
        use_parallel_computing: bool, optional
            Flag indicating whether to use parallel computing.
        """
        if not use_parallel_computing:
            for doc in docs: self._index_text(doc)
            return

        print("Using pool to index documents.")
        num_processes = os.cpu_count()

        with ProcessPoolExecutor(num_processes) as executor:
            executor.map(self._index_text, docs)
