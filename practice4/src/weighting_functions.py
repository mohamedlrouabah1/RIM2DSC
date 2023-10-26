"""
Define the classes for the indexing of the documents.
"""
import math



# Define the SMART ltn weighting function
def smart_ltn_weight(tf, df, N):
    return (1 + math.log(tf)) * math.log(N / df) if df > 0 and N > df else 0

# Define the SMART ltc weighting function
def smart_ltc_weight(tf, all_tf):
    tf_prime = 1 + math.log(tf) if tf > 0 else 0
    normalization = math.sqrt(sum((1 + math.log(k)) ** 2 for k in all_tf))
    return tf_prime / normalization if normalization != 0 else 0

# Define the BM25 weighting function
def bm25_weight(tf, df, N, doc_len, avg_doc_len, k1, b):
    # TODO : remove the if  for idf
    # TODO : compute the idf outside for not recomputing it for each document bc depend on the collection and not the document neither the term.
    # thus it prevent to compute it for each document and save time
    idf = math.log((N - df + 0.5) / (df + 0.5)) if df > 0 else 0
    tf_weight = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / avg_doc_len)))
    return tf_weight * idf
