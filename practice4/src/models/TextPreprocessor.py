import copyreg
import os
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
    # get stopwords from stopwords package
    # os.path.join(os.path.dirname(__file__), STOPWORDS_DIR)

    def _identity(x):
        return x

    def __init__(self, exclude_stopwords=True, exclude_digits=True, tokenizer="nltk", lemmer=None, stemmer=None, collection_pattern=None):
        if exclude_stopwords:
            #self.stopwords = set(stopwords.words('english') + list(punctuation))
            with open(STOPWORDS_DIR, 'r') as f:
                self.stopwords = set(f.read().splitlines() + list(punctuation))
        else:
            self.stopwords = set()

        # if exclude_digits:
        #     self.is_valid_token = lambda w: w.isalpha() and w not in self.stopwords
        # else:
        #     self.is_valid_token = lambda w: w not in self.stopwords
        

        # if tokenizer == "regex":
        #     # self.tokenize = lambda text: re.findall(r"\b\w+(?:'\w+)?\b", text)
        # else: 
        #     #tokenizer == "nltk"
        #     # self.tokenize = lambda text: word_tokenize(text)

        # lamda function don't work with // computation bc its use pickle
        # if lemmer and stemmer:
        #     self.lemmatizer = WordNetLemmatizer()
        #     self.stemmer = PorterStemmer()
        #     self.normalize = lambda w : self.stemmer.stem(self.lemmatizer.lemmatize(w))
        # elif lemmer:
        #     self.lemmatizer = WordNetLemmatizer()
        #     self.normalize = lambda w : self.lemmatizer.lemmatize(w)
        # elif stemmer:
        #     self.stemmer = PorterStemmer()
        #     self.normalize = lambda w : self.stemmer.stem(w)
        # else:
        #     self.normalize = lambda w : w
        if lemmer:
            self.lemmatizer = WordNetLemmatizer()
            self.lemmatizing = self.lemmatizer.lemmatize
        else:
            self.lemmatizing = TextPreprocessor._identity

        if stemmer:
            self.stemmer = PorterStemmer()
            self.stemming = self.stemmer.stem
        else:
            self.stemming = TextPreprocessor._identity

        if collection_pattern:
            self.collection_pattern = collection_pattern
        else:
            self.collection_pattern = re.compile(r'<doc><docno>(.*?)</docno>(.*?)</doc>', re.DOTALL)

    def normalize(self, w):
        return self.stemming(self.lemmatizing(w))
    
    def tokenize(self, w):
        return word_tokenize(w)
    
    def is_valid_token(self, w):
        return w.isalpha() and w not in self.stopwords


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
    
    def doc_preprocessing(self, doc):
        return [
            self.normalize(token)
            for token in self.tokenize(doc)
            if self.is_valid_token(token)
        ]
    
    def _preprocessing(self, doc_id, content):
        return (doc_id, self.doc_preprocessing(content))

    def pre_process(self, data, use_parallel_computing=False):
        # use_parallel_computing = False # For now bc pbm with pickle instance of this class
        if not use_parallel_computing :
            return [
                (doc_id, self.doc_preprocessing(content))
                for doc_id, content in tqdm(self.collection_pattern.findall(data), 
                                            desc="Preprocessing contents...", 
                                            colour="blue")
            ]
        
        # compute it using parallel computing
        print("Using pool to preprocess documents...")
        num_processes = os.cpu_count()
        # preprocessing = lambda doc : (doc[0], self.doc_preprocessing(doc[1]))

        with Pool(num_processes) as executor:
            results = executor.starmap(self._preprocessing, self.collection_pattern.findall(data))

        # results, remainnings = wait(results, return_when=ALL_COMPLETED)

        preprocessing = None
        # if remainnings is not None:
        #     print(f"{len(remainnings)} tasks not completed.")

        # NB: when we quit the with block automatically wait all future objects
        return list(results)