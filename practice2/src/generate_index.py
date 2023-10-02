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
# with stemming and stopword from nltk
def generate_index_oop(doc,value) -> Index:
    # Initialize the inverted index and doc frequency dictionaries
    index = Index()
    
    # This regex pattern will capture the doc_id and the content for each document in the collection
    doc_pattern = re.compile(r'<doc><docno>(.*?)</docno>(.*?)</doc>', re.DOTALL)
    
    # Loop through each document to update the inverted index and doc frequency
    for doc_id, content in doc_pattern.findall(doc):
        document = Document(doc_id, content)
        index.collection.add_document(document)
        # steeming + stop work test
        if value == 1:
            # stopwords from nltk
            tokens = [word for word in word_tokenize(content.lower()) if word.lower() not in stop_words  and word not in string.punctuation]
            # Apply Porter Stemming to each token
            choosed_tokens = [stemmer.stem(token) for token in tokens]   
        # # stemming + none stop word
        # if value == 4:
        #     # Convert to lowercase, tokenize, and remove non-alphanumeric characters all at once
        #     tokens = re.findall(r'\b[a-z0-9]+\b', content.lower())
        #     # Apply Porter Stemming to each token
        #     choosed_tokens = [stemmer.stem(token) for token in tokens]
        # none stemming + stop word only
        if value == 2:
            # stopwords from nltk
            tokens = [word for word in word_tokenize(content.lower()) if word.lower() not in stop_words  and word not in string.punctuation]
            choosed_tokens = tokens
        # none stemming + none stop word
        if value == 3:
            # Convert to lowercase, tokenize, and remove non-alphanumeric characters all at once
            tokens = re.findall(r'\b[a-z0-9]+\b', content.lower())
            choosed_tokens = tokens

        # Calculate term frequency for this document
        cf = Counter(choosed_tokens)

        
        # Update the inverted index and term frequency dictionary
        for term, freq in cf.items():
            unit = PostingListUnit(doc_id, freq)
            if index.posting_lists.get(term) is None:
                index.posting_lists[term] = PostingList(term)
            index.posting_lists[term].add_posting(unit)

    
    return index

def get_index_statistics(index):
    """
    Computes and returns statistics for the given index.
    """
    avg_doc_len = sum(d.length for d in index.collection.documents) / len(index.collection.documents)
    avg_term_len = sum(len(term) for term in index.get_vocabulary()) / index.get_vocabulary_size()
    vocab_size = index.get_vocabulary_size()
    total_coll_freq = sum(index.get_term_frequency(term) for term in index.get_vocabulary())
    return (avg_doc_len, avg_term_len, vocab_size, total_coll_freq)

if __name__ == "__main__":
    print("module generate_index.py not executable.")
