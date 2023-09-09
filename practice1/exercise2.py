import re
from collections import defaultdict, Counter

# Function to build inverted index
def build_inverted_index(document_collection_str):
    # Initialize inverted index and term frequency dictionaries
    inverted_index = defaultdict(list)
    term_frequency = defaultdict(lambda: defaultdict(int))

    # Parse the document_collection_str to get individual documents
    document_list = re.findall(r'<doc><docno>(.*?)</docno>(.*?)</doc>', document_collection_str)
    
    # Loop through each document to update inverted index and term frequency
    for doc_id, content in document_list:
        # Convert to lowercase and remove special characters
        content = content.lower()
        content = re.sub(r"[^a-zA-Z0-9\s]", "", content)
        
        # Tokenize the document
        tokens = content.split()
        
        # Count term frequency in this document
        tf = Counter(tokens)
        
        # Update term frequency dictionary
        for term, freq in tf.items():
            term_frequency[term][doc_id] = freq
            
        # Update inverted index
        for term in set(tokens):
            inverted_index[term].append(doc_id)
            
    return inverted_index, term_frequency, [doc_id for doc_id, _ in document_list]
