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
                posting.weight = smart_ltc_weight(tf, idf, all_tf, N)
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
                query_weights[term] = smart_ltc_weight(tf, idf, all_tf, N)
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

# # Relevance scores for SMART ltn weighting
# scores_smart_ltn = [68.73675449433486, 60.535267787308086, 60.24045204692686, 59.74489846805299, 59.5920192796959, 59.457820417764644, 57.85867204704381, 57.65866295936529, 57.499589051471624, 56.89693162380052]

# # Relevance scores for BM25 weighting
# scores_bm25 = [60.184592003278354, 56.075415224821555, 54.27455612878974, 53.68397186478026, 53.346998267048264, 52.106977013076325, 51.94257011579035, 51.73739303283615, 51.731835727091756, 51.71394050954665]

# # Document IDs for the top 10 documents (you can replace these with the actual document IDs)
# document_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# # Create a bar plot to compare the relevance scores
# plt.figure(figsize=(10, 6))
# plt.bar(document_ids, scores_smart_ltn, width=0.4, label='SMART ltn', align='center', alpha=0.7, color='b')
# plt.bar([d + 0.4 for d in document_ids], scores_bm25, width=0.4, label='BM25', align='center', alpha=0.7, color='g')
# plt.xlabel('Document IDs')
# plt.ylabel('Relevance Score (%)')
# plt.title('Comparison of Relevance Scores (Top 10 Documents)')
# plt.xticks([d + 0.2 for d in document_ids], document_ids)
# plt.legend(loc='upper right')
# plt.tight_layout()

# # Show the plot
# plt.show()
