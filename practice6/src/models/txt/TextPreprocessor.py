import copyreg
import os
import sys
import re
import types
from multiprocessing import Pool
from typing import Any
from nltk import word_tokenize, PorterStemmer, WordNetLemmatizer
# from nltk.corpus import stopwords
from string import punctuation
from tqdm import tqdm
from utilities.config import STOPWORDS_DIR

def _pickle_method(method):
    attached_object = method.im_self or method.im_class
    func_name = method.im_func.func_name

    if func_name.startswith('pre_'):
        func_name = filter(lambda method_name: method_name.startswith('_') and method_name.endswith(func_name), dir(attached_object))[0]

    return (getattr, (attached_object, func_name))
        
copyreg.pickle(types.MethodType, _pickle_method)

class TextPreprocessor:
    
    def __init__(self, exclude_stopwords=True, exclude_digits=True, tokenizer="nltk", lemmer=None, stemmer="None", collection_pattern=None):
        if exclude_stopwords:
            with open(STOPWORDS_DIR, 'r') as f:
                self.stopwords = set(f.read().splitlines() + list(punctuation)) 
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
        Read the document collection from a file.
        Handles both regular and gzipped files.

        Returns:
            str: the document collection as a lowered 
                 string
        """
        with open(path, 'r') as f:
            document_collection_str = f.read().lower()
        return document_collection_str

    def pre_process(self, data, use_parallel_computing=False):
        # use_parallel_computing = False # For now bc pbm with pickle instance of this class
        if not use_parallel_computing :
            return [
                (doc_id, self._text_preprocessing(content))
                for doc_id, content in tqdm(self.collection_pattern.findall(data), 
                                            desc="Preprocessing contents...", 
                                            colour="blue")
            ]
        
        # compute it using parallel computing
        print("Using pool to preprocess documents...")
        num_processes = os.cpu_count()

        with Pool(num_processes) as executor:
            results = executor.starmap(self._preprocessing, self.collection_pattern.findall(data))

        # NB: when we quit the with block automatically wait all future objects
        return list(results)