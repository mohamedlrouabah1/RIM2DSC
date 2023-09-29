import re
from collections import defaultdict, Counter
from models import *
import string


import nltk
from nltk import word_tokenize
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

from nltk import PorterStemmer
stemmer = PorterStemmer()

def generate_index(doc):
    # Initialize the inverted index and doc frequency dictionaries
    index = defaultdict(set)  # Using set to avoid duplicate doc_ids
    tf = defaultdict(lambda: defaultdict(int))
    
    # This regex pattern will capture the doc_id and the content for each document in the collection
    doc_pattern = re.compile(r'<doc><docno>(.*?)</docno>(.*?)</doc>', re.DOTALL)
    
    # Loop through each document to update the inverted index and doc frequency
    for doc_id, content in doc_pattern.findall(doc):
        
        # Convert to lowercase, tokenize, and remove non-alphanumeric characters all at once
        #tokens = re.findall(r'\b[a-z0-9]+\b', content.lower())
        # tokens = word_tokenize(text)
        #tokens = [token for token in tokens if token not in stop_words]
        tokens = [word for word in word_tokenize(content.lower()) if word.lower() not in stop_words  and word not in string.punctuation]
        
        # Calculate term frequency for this document
        cf = Counter(tokens)

        # Apply Porter Stemming to each token
        stemmed_tokens = [stemmer.stem(token) for token in tokens]

        # Update the inverted index and term frequency dictionary
        for term, freq in cf.items():
            tf[term][doc_id] = freq
            index[term].add(doc_id)

    # Convert index entries from sets to lists
    for term in index:
        index[term] = list(index[term])
    
    return index, tf, doc_id

def generate_index_oop(doc) -> Index:
    # Initialize the inverted index and doc frequency dictionaries
    index = Index()
    
    # This regex pattern will capture the doc_id and the content for each document in the collection
    doc_pattern = re.compile(r'<doc><docno>(.*?)</docno>(.*?)</doc>', re.DOTALL)
    
    # Loop through each document to update the inverted index and doc frequency
    for doc_id, content in doc_pattern.findall(doc):
        document = Document(doc_id, content)
        index.collection.add_document(document)
        
        # Convert to lowercase, tokenize, and remove non-alphanumeric characters all at once
        tokens = re.findall(r'\b[a-z0-9]+\b', content.lower())
        
        # Calculate term frequency for this document
        cf = Counter(tokens)

        # Update the inverted index and term frequency dictionary
        for term, freq in cf.items():
            unit = PostingListUnit(doc_id, freq)
            if index.posting_lists.get(term) is None:
                index.posting_lists[term] = PostingList(term)
            index.posting_lists[term].add_posting(unit)

    
    return index

if __name__ == "__main__":
    print("module generate_index.py not executable.")
