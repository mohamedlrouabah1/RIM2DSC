from collections import  Counter
import nltk
from nltk import PorterStemmer, WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import stopwords
import re
import string
from tqdm import tqdm
# from ply.lex_yacc_parser import *
from time import time_ns
from models.Index import Index
from models.Document import Document
from models.PostingList import PostingList
from models.PostingListUnit import PostingListUnit


nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def pre_processing(content, mode="basic"):
    tokens = [token for token in word_tokenize(content.lower()) if token not in string.punctuation]
    
    if mode == "nltk_stopwords":
        return [token for token in tokens if token not in stop_words]
    elif mode == "nltk_stopwords_stemmer":
        return [stemmer.stem(lemmatizer.lemmatize(token)) for token in tokens if token not in stop_words]
    elif mode == "stemmer":
        return [stemmer.stem(token) for token in tokens]
    elif mode == "basic":
        return tokens
    else:
        raise ValueError("Invalid mode provided!")

def generate_index_oop(doc, mode) -> Index:
    index = Index()
    
    doc_pattern = re.compile(r'<doc><docno>(.*?)</docno>(.*?)</doc>', re.DOTALL)

    # Mesurez le temps de prétraitement
    start_preprocessing_time_ns = time_ns()
    processed_contents = [(doc_id, pre_processing(content, mode)) 
                      for doc_id, content in tqdm(doc_pattern.findall(doc), desc="Preprocessing contents...", colour="blue")]
    index.preprocessing_time_in_ns = time_ns() - start_preprocessing_time_ns

    # Mesurez le temps d'indexation
    start_indexing_time_ns = time_ns()
    for doc_id, tokens in tqdm(processed_contents, desc="indexing files...", colour="green"):
        document = Document(doc_id, " ".join(tokens))
        index.collection.add_document(document)
        cf = Counter(tokens)
        for term, freq in cf.items():
            unit = PostingListUnit(doc_id, freq)
            if index.posting_lists.get(term) is None:
                index.posting_lists[term] = PostingList(term)
            index.posting_lists[term].add_posting(unit)
    
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
