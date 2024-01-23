from __future__ import annotations
import copyreg
import os
import sys
import re
import types
from multiprocessing import Pool

from string import punctuation
from nltk import word_tokenize, PorterStemmer, WordNetLemmatizer
from tqdm import tqdm
from utilities.config import STOPWORDS_DIR

def _pickle_method(method):
    attached_object = method.im_self or method.im_class
    func_name = method.im_func.func_name

    if func_name.startswith('pre_'):
        func_name = filter(lambda method_name: method_name.startswith('_') and method_name.endswith(func_name), dir(attached_object))

    return (getattr, (attached_object, func_name))

copyreg.pickle(types.MethodType, _pickle_method)

class TextPreprocessor:
    """
    Preprocessor for text documents.

    Attributes:
        - stopwords (set): Set of stopwords to be excluded from processing.
        - lemmatizer (WordNetLemmatizer): WordNet lemmatizer.
        - lemmatizing (function): Function for lemmatization.
        - stemming (function): Function for stemming.
        - stemmer (PorterStemmer): Porter stemmer.
        - collection_pattern (re.Pattern): Regular expression pattern for identifying document collections.
        - exclude_digits (bool): Flag indicating whether to exclude digits from processing.
        - tokenizer_name (str): Name of the tokenizer used.

    Methods:
        __init__(exclude_stopwords=True, exclude_digits=True, tokenizer="nltk", lemmer=None, stemmer="None", collection_pattern=None): Initializes the TextPreprocessor object.
        _identity(x): Identity function.
        _normalize(w: str) -> str: Normalizes a word by applying lemmatization and stemming.
        _tokenize(w: str): Tokenizes a word using the specified tokenizer.
        _is_valid_token(w: str) -> bool: Checks if a token is valid based on length, alphabetical characters, and exclusion from stopwords.
        _text_preprocessing(text: str) -> list[str]: Performs text preprocessing by normalizing and tokenizing.
        _preprocessing(doc_id, content) -> tuple: Used for parallel computing, performs preprocessing for a document.
        load_and_lower_text_collection(path) -> str: Reads the document collection from a file and converts it to lowercase.
        pre_process(raw_collection, use_parallel_computing=False) -> list[tuple]: Performs preprocessing on the entire collection.

    """

    def __init__(self, exclude_stopwords=True, exclude_digits=True, tokenizer="nltk", lemmer=None, stemmer="None", collection_pattern=None):
        """
        Initializes the TextPreprocessor object.

        Params:
        -------
        exclude_stopwords (bool, optional): Flag indicating whether to exclude stopwords. Defaults to True.
        exclude_digits (bool, optional): Flag indicating whether to exclude digits. Defaults to True.
        tokenizer (str, optional): Name of the tokenizer. Defaults to "nltk".
        lemmer: Lemmatizer (WordNetLemmatizer), optional: Lemmatizer to be used. Defaults to None.
        stemmer (str, optional): Type of stemmer. Defaults to "None".
        collection_pattern (re.Pattern, optional): Regular expression pattern for identifying document collections. Defaults to None.

        """
        if exclude_stopwords:
            self.stopwords = set()
            for file_path in os.listdir(STOPWORDS_DIR):
                with open(f"{STOPWORDS_DIR}/{file_path}", 'r', encoding="utf-8") as f:
                    self.stopwords = self.stopwords.union(set(f.read().splitlines()))

            self.stopwords = self.stopwords.union(set(punctuation))
            print(f"Stopwords loaded from {STOPWORDS_DIR} with {len(self.stopwords)} words.", file=sys.stderr)
        else:
            print("Error, unnable to load stopwords.", file=sys.stderr)
            self.stopwords = set()

        if lemmer:
            self.lemmatizer = WordNetLemmatizer()
            self.lemmatizing = self.lemmatizer.lemmatize
        else:
            self.lemmatizing = self._identity

        if stemmer == "None":
            self.stemming = self._identity
        else:
            self.stemmer = PorterStemmer()
            self.stemming = self.stemmer.stem

        if collection_pattern:
            self.collection_pattern = collection_pattern
        else:
            self.collection_pattern = re.compile(r'<doc><docno>(.*?)</docno>(.*?)</doc>', re.DOTALL)

        self.exclude_digits = exclude_digits
        self.tokenizer_name = tokenizer

    def _identity(self, x):
        return x

    def _normalize(self, w:str) -> str:
        return self.stemming(self.lemmatizing(w))

    def _tokenize(self, w:str):
        return word_tokenize(w)

    def _is_valid_token(self, w:str) -> bool:
        return len(w) > 2 and w.isalpha() and w not in self.stopwords

    def _text_preprocessing(self, text:str):
        return [
            self._normalize(token)
            for token in self._tokenize(text)
            if self._is_valid_token(token)
        ]

    def _preprocessing(self, doc_id, content):
        """Used for the parallel computing"""
        return (doc_id, self._text_preprocessing(content))

    def load_and_lower_text_collection(self, path) -> str:
        """
        Reads the document collection from a file and converts it to lowercase.

        Params:
        -------
        path: str
            Path to the document collection file.

        Returns:
        --------
        str: Lowercased document collection as a string.

        """
        with open(path, 'r', encoding="utf-8") as f:
            document_collection_str = f.read().lower()
        return document_collection_str

    def pre_process(self, raw_collection, use_parallel_computing=False) -> list[tuple[str, list[str]]]:
        """
        Performs preprocessing on the entire collection.

        Params:
        -------
        raw_collection: str
            Raw document collection.
        use_parallel_computing (bool, optional): Flag indicating whether to use parallel computing. Defaults to False.

        Returns:
        --------
        list[tuple]: List of tuples containing document identifier and preprocessed content.

        """
        # use_parallel_computing = False # For now bc pbm with pickle instance of this class
        if not use_parallel_computing :
            return [
                (doc_id, self._text_preprocessing(content))
                for doc_id, content in tqdm(self.collection_pattern.findall(raw_collection),
                                            desc="Preprocessing contents...",
                                            colour="blue")
            ]

        # compute it using parallel computing
        print("Using pool to preprocess documents...")
        num_processes = os.cpu_count()

        with Pool(num_processes) as executor:
            results = executor.starmap(self._preprocessing, self.collection_pattern.findall(raw_collection))

        # NB: when we quit the with block automatically wait all future objects
        return list(results)
