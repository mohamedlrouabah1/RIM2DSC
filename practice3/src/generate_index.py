from collections import  Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
import time

from nltk import PorterStemmer, word_tokenize
import re
from tqdm import tqdm
# from ply.lex_yacc_parser import *
from time import time_ns
from models.Index import Index
from models.Document import Document
from models.PostingList import PostingList
from models.PostingListUnit import PostingListUnit
from pathlib import Path
stemmer = PorterStemmer()

def pre_processing(content : str, mode="stopwords_stemmer") -> list:
    stop_words = set(Path("../../stopwords/stop-words-english4.txt").read_text(encoding="utf-8"))
    if mode == "stopwords_stemmer":
        return [stemmer.stem(token)
                for token in word_tokenize(content)
                if token.isalpha() and token not in stop_words]   
    elif mode == "stemmer":
        return [stemmer.stem(token) for token in word_tokenize(content) if token.isalpha() and token not in stop_words]
    elif mode == "basic":
        return [token for token in  word_tokenize(content) if token.isalpha() and token not in stop_words]
    else:
        raise ValueError("Invalid mode provided!")

def index_document(args):
    """Helper function to handle the parallel indexing of a document."""
    doc_id, tokens, index = args
    
    document = Document(doc_id, " ".join(tokens))
    index.collection.add_document(document)
    cf = Counter(tokens)
    for term, freq in cf.items():
        unit = PostingListUnit(doc_id, freq)
        if term not in index.posting_lists:
            index.posting_lists[term] = PostingList(term)
        index.posting_lists[term].add_posting(unit)
    return index

def preprocess_document(args):
    """Helper function to handle the parallel processing of documents."""
    doc_id, content, mode = args
    return (doc_id, pre_processing(content, mode))

def generate_index_oop(doc, mode) -> Index:
    index = Index()
    doc_pattern = re.compile(r'<doc><docno>(.*?)</docno>(.*?)</doc>', re.DOTALL)
    
    # Extract all document patterns
    doc_matches = doc_pattern.findall(doc)
    
    # Measure preprocessing time with parallel processing and tqdm for progress
    start_preprocessing_time_ns = time_ns()
    processed_contents = []
    with ProcessPoolExecutor() as executor:
        # Using submit for preprocessing
        futures = [executor.submit(preprocess_document, (match[0], match[1], mode)) for match in doc_matches]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Preprocessing documents...", colour="blue"):
            processed_contents.append(future.result())
    index.preprocessing_time_in_ns = time_ns() - start_preprocessing_time_ns

    # Measure indexing time with parallel processing
    start_indexing_time_ns = time_ns()
    with ProcessPoolExecutor() as executor:
        # Using submit for indexing
        futures = [executor.submit(index_document, (doc_id, tokens, index)) for doc_id, tokens in processed_contents]
        for future in tqdm(as_completed(futures), total=len(futures), desc="indexing files...", colour="green"):
            # Here, we're getting back the indexed data from each process
            # In this specific case, we don't need to do anything with the results
            # because the index object is shared and modified in-place.
            future.result()
    index.indexing_time_in_ns = time_ns() - start_indexing_time_ns

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
