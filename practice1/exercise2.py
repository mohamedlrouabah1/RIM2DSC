import re
from collections import defaultdict, Counter
import pandas as pd

# functiond to generate the inverted index
def generate_index(doc):
    # init the inverted index and doc frequency dictionaries
    index = defaultdict(list)
    tf = defaultdict(lambda: defaultdict(int))

    # parse the document to get individual documents
    parse_doc = re.findall(r'<doc><docno>(.*?)</docno>(.*?)</doc>', doc)
    
    # loop each document to update the inverted index and doc frequency
    for doc_id, content in parse_doc:
        # Convert to lowercase and remove special characters
        content = content.lower()
        content = re.sub(r"[^a-zA-Z0-9\s]", "", content)
        # Tokenize the document
        tokens = content.split()
        # Count doc frequency in this document
        cf = Counter(tokens)

        # Update doc frequency dictionary
        for term, freq in cf.items():
            tf[term][doc_id] = freq    
        
        # Update inverted index
        for term in set(tokens):
            index[term].append(doc_id)
        # store the doc_ids for query usecase
        doc_ids = doc_id

    res = index, tf, doc_ids
    return res