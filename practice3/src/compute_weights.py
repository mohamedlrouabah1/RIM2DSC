import math
import matplotlib.pyplot as plt
import os


from generate_index import option_execution
from utilities.config import GRAPH_FOLDER
from weighting_functions import bm25_weight, smart_ltc_weight, smart_ltn_weight



def compute_weights(index, weighting_function) -> None:
    """
    Function to compute weights for the terms in the document collection
    """
    N = len(index.collection.documents)
    avg_doc_len = sum(d.length for d in index.collection.documents) / N
    
    for term, posting_list in index.posting_lists.items():
        df = posting_list.document_frequency
        
        for doc_id, posting in posting_list.postings.items():
            tf = posting.frequency
            
            if weighting_function == smart_ltn_weight:
                posting.weight = smart_ltn_weight(tf, df, N)
            elif weighting_function == smart_ltc_weight:
                all_tf = [p.frequency for p in posting_list.postings.values()]
                posting.weight = smart_ltc_weight(tf, all_tf)
            elif weighting_function == bm25_weight:
                doc_len = 1
                posting.weight = bm25_weight(tf, df, N, doc_len, avg_doc_len)


def compute_query_weights(query, index, weighting_function) -> dict:
    """
    Function to compute query weights using a weighting function
    """
    tokenized_query = option_execution(query)  # Use the preprocessing function
    N = len(index.collection.documents)
    query_weights = {}
    
    for term in tokenized_query:
        if term in index.posting_lists:
            df = index.posting_lists[term].document_frequency
            tf = 1  # Assuming tf for the query term is 1
            
            if weighting_function == smart_ltn_weight:
                query_weights[term] = smart_ltn_weight(tf, df, N)
            elif weighting_function == smart_ltc_weight:
                all_tf = [p.frequency for p in index.posting_lists[term].postings.values()]
                query_weights[term] = smart_ltc_weight(tf, all_tf)
            elif weighting_function == bm25_weight:
                doc_len = 1
                avg_doc_len = sum(d.length for d in index.collection.documents) / N
                query_weights[term] = bm25_weight(tf, df, N, doc_len, avg_doc_len)

    
    return query_weights

def compute_rank_documents(query_weights, index) -> list:
    """
    Function to compute the score of each document using a weighting function
    """
    scores = {}
    
    for term, weight in query_weights.items():
        if term in index.posting_lists:
            for doc_id, posting in index.posting_lists[term].postings.items():
                doc_weight = posting.weight
                
                if doc_id not in scores:
                    scores[doc_id] = 0
                scores[doc_id] += weight * doc_weight

    # Sort documents by their IDs in ascending order
    ranked_docs = sorted(scores.items(), key=lambda x: x[0])
    return ranked_docs


def smart_ltn(query, index, top_k) -> list:
    """Compute weights for the index using SMART ltn weighting"""
    compute_weights(index, smart_ltn_weight)

    
    query_weights_ltn = compute_query_weights(query, index, smart_ltn_weight)
    ranked_docs_ltn = compute_rank_documents(query_weights_ltn, index)

    print("Top 10 documents using SMART ltn weighting:")
    for doc_id, score in ranked_docs_ltn[:top_k]:
        print(f"Document ID: {doc_id}, Relevance Score: {score} correspondancy to the query executed")
    
    return ranked_docs_ltn


def smart_ltc(query, index, top_k):
    # Compute weights for the index using SMART ltc weighting
    # compute_weights(index, smart_ltc_weight)
    # Retrieve and print the top 10 most relevant documents using SMART ltc weighting
    query_weights_ltc = compute_query_weights(query, index, smart_ltc_weight)
    ranked_docs_ltc = compute_rank_documents(query_weights_ltc, index)

    print("Top 10 documents using SMART ltc weighting:")
    for doc_id, score in ranked_docs_ltc[:top_k]:
        print(f"Document ID: {doc_id}, Relevance Score: {score} correspondancy to the query executed")
    
    return ranked_docs_ltc


def smart_bm25(query, index, top_k):
    """Compute weights for the index using BM25 weighting"""
    compute_weights(index, bm25_weight)
    
    query_weights_bm25 = compute_query_weights(query, index, bm25_weight)
    ranked_docs_bm25 = compute_rank_documents(query_weights_bm25, index)

    print("Top 10 documents using BM25 weighting:")
    for doc_id, score in ranked_docs_bm25[:top_k]:
        print(f"Document ID: {doc_id}, Relevance Score: {score} correspondance to the query executed")
    
    return ranked_docs_bm25

def plot_relevance_score(ranked_docs_ltn,ranked_docs_bm25, top_k):  
    # Extract the document IDs and relevance scores from ranked_docs
    document_ids_ltn = [doc_id for doc_id, _ in ranked_docs_ltn[:top_k]]
    relevance_scores_ltn = [score for _, score in ranked_docs_ltn[:top_k]]

    document_ids_bm25 = [doc_id for doc_id, _ in ranked_docs_bm25[:top_k]]
    relevance_scores_bm25 = [score for _, score in ranked_docs_bm25[:top_k]]

    # Create a line plot for SMART LTN
    plt.plot(document_ids_ltn, relevance_scores_ltn, marker='o', label='SMART LTN', color='b')

    # Create a line plot for BM25
    plt.plot(document_ids_bm25, relevance_scores_bm25, marker='o', label='BM25', color='r')

    # Add labels and a legend
    plt.xlabel("Document ID")
    plt.ylabel("Relevance Score")
    plt.title("Relevance Score Comparison for Different Query Methods")
    plt.legend()

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Show the plot
    plt.grid(True)
    plt.savefig(os.path.join(GRAPH_FOLDER, f"Relevance_Score_Comparison_for_Different_Query_Methods.png"))
    plt.show()
