from collections import defaultdict
import re

# Initialize the inverted index and document frequencies
inverted_index = defaultdict(list)
document_freq = defaultdict(int)

# Read the input document containing the collection
with open("exercise1_collection.txt", "r") as file:
    content = file.read()

# Split the content into documents based on the <doc> and </doc> tags
documents = re.split(r'<doc><docno>D\d+</docno>', content)
documents = [doc.strip('</doc>') for doc in documents if doc]

# Process each document
for doc in documents:
    lines = doc.split('\n')
    doc_id = lines[0].strip()  # Extract the document identifier
    text = ' '.join(lines[1:]).lower()  # Extract and normalize the text

    # Tokenize the text by whitespace
    terms = text.split()

    # Calculate the term frequencies (tf) for this document
    term_freq = defaultdict(int)
    for term in terms:
        term_freq[term] += 1

    # Update the inverted index and document frequencies
    for term, freq in term_freq.items():
        inverted_index[term].append((doc_id, freq))
        document_freq[term] += 1

# Print the inverted index with document frequencies
for term, postings in inverted_index.items():
    df = document_freq[term]
    print(f"{df}=df({term})")
    for doc_id, tf in postings:
        print(f"{tf} {doc_id}")

# Optionally, you can save the inverted index to a file or serve it via Flask.
