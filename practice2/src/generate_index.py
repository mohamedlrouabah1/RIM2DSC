import re
from collections import defaultdict, Counter

def generate_index(doc):
    # Initialize the inverted index and doc frequency dictionaries
    index = defaultdict(set)  # Using set to avoid duplicate doc_ids
    tf = defaultdict(lambda: defaultdict(int))
    
    # This regex pattern will capture the doc_id and the content for each document in the collection
    doc_pattern = re.compile(r'<doc><docno>(.*?)</docno>(.*?)</doc>', re.DOTALL)
    
    # Loop through each document to update the inverted index and doc frequency
    for doc_id, content in doc_pattern.findall(doc):
        
        # Convert to lowercase, tokenize, and remove non-alphanumeric characters all at once
        tokens = re.findall(r'\b[a-z0-9]+\b', content.lower())
        
        # Calculate term frequency for this document
        cf = Counter(tokens)

        # Update the inverted index and term frequency dictionary
        for term, freq in cf.items():
            tf[term][doc_id] = freq
            index[term].add(doc_id)

    # Convert index entries from sets to lists
    for term in index:
        index[term] = list(index[term])
    
    return index, tf, doc_id

if __name__ == "__main__":
    print("module generate_index.py not executable.")
