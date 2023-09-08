from collections import defaultdict
import re

# Initialize the inverted index and document frequencies
inverted_index = defaultdict(list)
document_freq = defaultdict(int)

# Read the input document containing the collection
with open("exercise1_collection.txt", "r", encoding="utf-8") as file:
    content = file.read()
    
print(content)
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

# Save the inverted index to a file
with open("inverted_index.txt", "w") as index_file:
    for term, postings in inverted_index.items():
        df = document_freq[term]
        index_file.write(f"{df}=df({term})\n")
        for doc_id, tf in postings:
            index_file.write(f"{tf} {doc_id}\n")

# Function to execute an AND query
def execute_and(query, stack):
    operand2 = stack.pop()
    operand1 = stack.pop()
    result = set(operand1).intersection(operand2)
    stack.append(result)

# Function to execute an OR query
def execute_or(query, stack):
    operand2 = stack.pop()
    operand1 = stack.pop()
    result = set(operand1).union(operand2)
    stack.append(result)

# Function to execute a NOT query
def execute_not(query, stack):
    operand = stack.pop()
    result = set(document_ids) - set(operand)
    stack.append(result)

# Function to execute a term query
def execute_term(query, stack):
    document_ids = [doc_id for _, doc_id in inverted_index.get(query, [])]
    stack.append(document_ids)

# Dictionary mapping operators to execution functions
operators = {
    'and': execute_and,
    'or': execute_or,
    'not': execute_not
}

# Function to execute a boolean query
def execute_boolean_query(query):
    stack = []  # Stack to evaluate the query
    query = query.lower().split()  # Normalize and split the query

    for term in query:
        if term in operators:
            if len(stack) < 2:
                print("Error: Insufficient operands for operator", term)
                return []
            operators[term](term, stack)
        else:
            execute_term(term, stack)

    # The final result should be on the stack
    if stack:
        return list(stack[0])
    else:
        return []

# Example queries
query1 = "casablanca and godfather"
query2 = "citizen or graduate"
query3 = "lawrence and not arabia"

# Execute and print the results
results = {}
results["Query 1"] = execute_boolean_query(query1)
results["Query 2"] = execute_boolean_query(query2)
results["Query 3"] = execute_boolean_query(query3)

# Save the results to a file
with open("query_results.txt", "w") as result_file:
    for query, result in results.items():
        result_file.write(f"{query}: {result}\n")

# Print the results
for query, result in results.items():
    print(query + ":", result)
