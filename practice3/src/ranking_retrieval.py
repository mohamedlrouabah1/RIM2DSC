import matplotlib.pyplot as plt
import math
import os

from generate_index import *
from utilities.config import GRAPH_FOLDER
from utilities.utils import *
from models import *


def retrieve_top_documents(query, mode_func, index, k1, b):
    # Tokenize the query
    query_tokens = option_execution(query, mode="basic")
    
    # Initialize a dictionary to store document scores
    document_scores = {}

    # Loop through each term in the query
    for term in tqdm(query_tokens, desc="ranking documents...", colour="green", leave=False):
        if term in index.posting_lists:
            df = index.posting_lists[term].document_frequency
            posting_list = index.posting_lists[term]
            for posting_unit in posting_list.postings.values():
                doc_id = posting_unit.document_id
                tf = posting_unit.frequency
                all_tf = [p.frequency for p in posting_list.postings.values()]
                N = len(index.collection.documents)

                if mode_func == "smart_ltn":
                    # Calculate the SMART ltn score for this term in the document
                    score = smart_ltn_weight(tf, df, N)
                elif mode_func == "smart_ltc":
                    # Calculate the SMART ltc score for this term in the document
                    score = smart_ltc_weight(tf, all_tf)
                elif mode_func == "bm25":
                    # Calculate the BM25 score for this term in the document
                    # If document length is null, set it to 0
                    doc_len = 0  

                    if doc_id in index.collection.documents:
                        doc_len = index.collection.documents[doc_id].length

                    total_doc_len = sum(document.length for document in index.collection.documents)
                    avg_doc_len = total_doc_len / len(index.collection.documents)
                    score = bm25_weight(tf, df, N, doc_len, avg_doc_len, k1, b)
                else:
                    raise ValueError("Invalid mode provided!")

                # Add the score to the document's total score
                if doc_id in document_scores:
                    document_scores[doc_id] += score
                else:
                    document_scores[doc_id] = score

    # Sort the documents by their scores in descending order
    sorted_documents = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)

    # Return the top 10 most relevant documents and their scores
    return sorted_documents[:10]


def print_ranking(query, scoring_mode, index, b, k1):  
    top_documents = retrieve_top_documents(query, scoring_mode, index, b, k1)

    # Print the top relevant documents and their scores
    for doc_id, score in top_documents:
        print(f"Document ID: {doc_id}, Score: {score}")


def plot_ranking(query, index, b, k1):
    scoring_modes = ["smart_ltn", "smart_ltc", "bm25"]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for i, scoring_mode in enumerate(scoring_modes):
        top_documents = retrieve_top_documents(query, scoring_mode, index, k1, b)
        doc_ids, scores = zip(*top_documents)

        ax = axes[i]
        ax.plot(range(1, 10 + 1), scores, marker='o', linestyle='-')
        ax.set_ylabel('Score')
        ax.set_title(scoring_mode.upper())

        # Rotate the document IDs by 45 degrees for better readability
        ax.set_xticks(range(1, 10 + 1))
        ax.set_xticklabels(doc_ids, rotation=45, ha='right')

    plt.suptitle('Top Documents Ranking Comparison')
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_FOLDER, f"Relevance_Score_Comparison_Query_Methods.png"))
    plt.show()
    