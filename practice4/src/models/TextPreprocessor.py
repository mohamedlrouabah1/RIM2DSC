import re
from nltk import word_tokenize, PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from string import punctuation
from tqdm import tqdm

class TextPreprocessor:

    def __init__(self, exclude_stopwords=True, exclude_digits=True, tokenizer="nltk", lemmer=None, stemmer=None, collection_pattern=None):
        if exclude_stopwords:
            self.stopwords = set(stopwords.words('english') + list(punctuation))
        else:
            self.stopwords = set()

        if exclude_digits:
            self.is_valid_token = lambda w: w.isalpha() and w not in self.stopwords
        else:
            self.is_valid_token = lambda w: w not in self.stopwords
        

        if tokenizer == "regex":
            self.tokenize = lambda text: re.findall(r"\b\w+(?:'\w+)?\b", text)
        else: 
            #tokenizer == "nltk"
            self.tokenize = lambda text: word_tokenize(text)

        if lemmer and stemmer:
            self.lemmatizer = WordNetLemmatizer()
            self.stemmer = PorterStemmer()
            self.normalize = lambda w : self.stemmer.stem(self.lemmatizer.lemmatize(w))
        elif lemmer:
            self.lemmatizer = WordNetLemmatizer()
            self.normalize = lambda w : self.lemmatizer.lemmatize(w)
        elif stemmer:
            self.stemmer = PorterStemmer()
            self.normalize = lambda w : self.stemmer.stem(w)
        else:
            self.normalize = lambda w : w

        if collection_pattern:
            self.collection_pattern = collection_pattern
        else:
            self.collection_pattern = re.compile(r'<doc><docno>(.*?)</docno>(.*?)</doc>', re.DOTALL)


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

    def pre_process(self, data):
        return [
            (doc_id, self.doc_preprocessing(content))
            for doc_id, content in tqdm(self.collection_pattern.findall(data), 
                                        desc="Preprocessing contents...", 
                                        colour="blue")
        ]