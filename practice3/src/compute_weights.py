from generate_index import *
from utils import *
from models import *
import math
import matplotlib.pyplot as plt

# Function to compute weights for the terms in the document collection
def compute_weights(index, weighting_function):
    N = len(index.collection.documents)
    avg_doc_len = sum(d.length for d in index.collection.documents) / N
    
    for term, posting_list in index.posting_lists.items():
        df = posting_list.document_frequency
        
        for doc_id, posting in posting_list.postings.items():
            tf = posting.frequency
            
            if weighting_function == smart_ltn_weight:
                posting.weight = smart_ltn_weight(tf, df, N)
            elif weighting_function == smart_ltc_weight:
                idf = math.log(N / df) if df > 0 and N > df else 0
                all_tf = [p.frequency for p in posting_list.postings.values()]
                posting.weight = smart_ltc_weight(tf, all_tf)
            elif weighting_function == bm25_weight:
                doc_len = 1
                posting.weight = bm25_weight(tf, df, N, doc_len, avg_doc_len)

# Function to compute query weights using a weighting function
def compute_query_weights(query, index, weighting_function):
    tokenized_query = option_execution(query)  # Use your preprocessing function
    N = len(index.collection.documents)
    query_weights = {}
    
    for term in tokenized_query:
        if term in index.posting_lists:
            df = index.posting_lists[term].document_frequency
            tf = 1  # Assuming tf for the query term is 1
            
            if weighting_function == smart_ltn_weight:
                query_weights[term] = smart_ltn_weight(tf, df, N)
            elif weighting_function == smart_ltc_weight:
                idf = math.log(N / df) if df > 0 and N > df else 0
                all_tf = [p.frequency for p in index.posting_lists[term].postings.values()]
                query_weights[term] = smart_ltc_weight(tf, all_tf)
            elif weighting_function == bm25_weight:
                doc_len = 1
                avg_doc_len = sum(d.length for d in index.collection.documents) / N
                query_weights[term] = bm25_weight(tf, df, N, doc_len, avg_doc_len)

    
    return query_weights

# Function to compute the score of each document using a weighting function
def compute_rank_documents(query_weights, index):
    scores = {}
    
    for term, weight in query_weights.items():
        if term in index.posting_lists:
            for doc_id, posting in index.posting_lists[term].postings.items():
                doc_weight = posting.weight
                
                if doc_id not in scores:
                    scores[doc_id] = 0
                scores[doc_id] += weight * doc_weight

    # Sort documents by their scores in descending order
    ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_docs

# Load the document collection and create the index
content = load_text_collection(f"{DATA_FOLDER}/{COLLECTION_FILES[0]}")
index = generate_index_oop(content, mode="basic")
query = "web ranking scoring algorithm"

# Retrieve and print the top 10 most relevant documents using SMART ltn weighting
top_k = 10

def smart_ltn():
    # Compute weights for the index using SMART ltn weighting
    compute_weights(index, smart_ltn_weight)

    
    query_weights_ltn = compute_query_weights(query, index, smart_ltn_weight)
    ranked_docs_ltn = compute_rank_documents(query_weights_ltn, index)

    print("Top 10 documents using SMART ltn weighting:")
    for doc_id, score in ranked_docs_ltn[:top_k]:
        print(f"Document ID: {doc_id}, Relevance Score: {score} % correspondancy to the query executed")

def smart_ltc():
    # Compute weights for the index using SMART ltc weighting
    compute_weights(index, smart_ltc_weight)
    # Retrieve and print the top 10 most relevant documents using SMART ltc weighting
    query_weights_ltc = compute_query_weights(query, index, smart_ltc_weight)
    ranked_docs_ltc = compute_rank_documents(query_weights_ltc, index)

    print("Top 10 documents using SMART ltc weighting:")
    for doc_id, score in ranked_docs_ltc[:top_k]:
        print(f"Document ID: {doc_id}, Relevance Score: {score} % correspondancy to the query executed")

def smart_bm25():
    # Compute weights for the index using BM25 weighting
    compute_weights(index, bm25_weight)
    
    query_weights_bm25 = compute_query_weights(query, index, bm25_weight)
    ranked_docs_bm25 = compute_rank_documents(query_weights_bm25, index)

    print("Top 10 documents using BM25 weighting:")
    for doc_id, score in ranked_docs_bm25[:top_k]:
        print(f"Document ID: {doc_id}, Relevance Score: {score} % correspondance to the query executed")

