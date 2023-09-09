import pandas as pd
from exercise2 import build_inverted_index  
from exercise3 import boolean_query_parser  

# Read the document collection from a file
with open('data/documentxml.xml', 'r') as f:
    document_collection_str = f.read()

# Build the inverted index, term frequencies, and document IDs
inverted_index, term_frequency, doc_ids = build_inverted_index(document_collection_str)

# Create DataFrame to hold the inverted index
df = pd.DataFrame(columns=['Term', 'DF', 'Postings List'])

# Create an empty list to hold rows
rows = []

# Populate the rows list
for term, postings_list in inverted_index.items():
    rows.append({
        'Term': term,
        'DF': len(postings_list),
        'Postings List': ", ".join([f"{term_frequency[term][doc_id]} {doc_id}" for doc_id in postings_list])
    })

# Create a DataFrame from the rows list
df = pd.DataFrame(rows)

# Export DataFrame to CSV
df.to_csv('data/resultInvertedIndex.csv', index=False)

# Read queries from query.txt file
with open('data/query_sample.txt', 'r') as f:
    sample_queries = f.read().strip().split('\n')

# Loop through the sample queries and print the results
for query in sample_queries:
    result = boolean_query_parser(query, inverted_index, doc_ids)
    print(f"For the query '{query}', the results are: {result}")