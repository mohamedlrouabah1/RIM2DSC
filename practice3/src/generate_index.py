from collections import  Counter
import nltk
from nltk import PorterStemmer
from nltk import word_tokenize
from nltk.corpus import stopwords
import re
import string
from tqdm import tqdm
# from ply.lex_yacc_parser import *

from models.Index import Index
from models.Document import Document
from models.PostingList import PostingList
from models.PostingListUnit import PostingListUnit


nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()


def option_execution(content, mode="basic"):
    if mode == "basic":
        return re.findall(r'\b[a-z0-9]+\b', content.lower())

    elif mode == "nltk_stopwords":
        return [word for word in word_tokenize(content.lower()) if word.lower() not in stop_words and word not in string.punctuation]

    elif mode == "nltk_stopwords_stemmer":
        tokens = [stemmer.stem(word)for word in word_tokenize(content.lower()) if word.lower() not in stop_words and word not in string.punctuation]
        return tokens
    
    elif mode == "stemmer":
        return [stemmer.stem(token) for token in word_tokenize(content.lower())]

    else:
        raise ValueError("Invalid mode provided!")

def generate_index_oop(doc, mode) -> Index:
    # Initialize the inverted index and doc frequency dictionaries
    index = Index()
    
    # This regex pattern will capture the doc_id and the content for each document in the collection
    doc_pattern = re.compile(r'<doc><docno>(.*?)</docno>(.*?)</doc>', re.DOTALL)
    # Use PLY to parse the document
    # doc_pattern = parser.parse(doc)

    # Loop through each document to update the inverted index and doc frequency
    for doc_id, content in tqdm(doc_pattern.findall(doc), desc="indexing files...", colour="green"):
        document = Document(doc_id, content)
        index.collection.add_document(document)

        # Apply tokenization to the document content
        token = option_execution(content,mode)

        # Calculate term frequency for this document
        cf = Counter(token)
        
        # Update the inverted index and term frequency dictionary
        for term, freq in cf.items():
            unit = PostingListUnit(doc_id, freq)
            if index.posting_lists.get(term) is None:
                index.posting_lists[term] = PostingList(term)
            index.posting_lists[term].add_posting(unit)
            # print(f"Parsing doc: {doc_id}")
            # print(f"First 10 terms in tokenized content: {token[:10]}")
            # print(f"Term frequencies for first 10 terms: {[cf.get(term, 0) for term in token[:10]]}")

    
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
