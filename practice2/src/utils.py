import pandas as pd
import gzip
import time
from generate_index import generate_index_oop
from utilities.time_utility import convert_time_from_ns_to_s

DATA_FOLDER="../../data"
RENDU_FOLDER="../../rendus"
COLLECTION_FILES = [
    '01-Text_Only-Ascii-Coll-1-10-NoSem.gz',
    '02-Text_Only-Ascii-Coll-11-20-NoSem.gz',
    '03-Text_Only-Ascii-Coll-21-50-NoSem.gz',
    '04-Text_Only-Ascii-Coll-51-100-NoSem.gz',
    '05-Text_Only-Ascii-Coll-101-200-NoSem.gz',
    '06-Text_Only-Ascii-Coll-201-500-NoSem.gz',
    '07-Text_Only-Ascii-Coll-501-1000-NoSem.gz',
    '08-Text_Only-Ascii-Coll-1001-2000-NoSem.gz',
    '09-Text_Only-Ascii-Coll-2001-5000-NoSem.gz'
]
    
def load_text_collection(path) -> str:
    """
    Read the document collection from a file.
    Handles both regular and gzipped files.
    """
    if path.endswith('.gz'):
        with gzip.open(path, 'rt', encoding='utf-8') as f:
            document_collection_str = f.read()
    else:
        with open(path, 'r') as f:
            document_collection_str = f.read()
    return document_collection_str

def generate_grid(index, mode: str) -> pd.DataFrame:
    """
    This function takes in an index object and generates a grid based on the mode.
    The mode can be either IDF or Query.
    If the mode is IDF, then the grid should contain the following columns:
    - Term
    - DF
    - Postings List
    If the mode is Query, then the grid should contain the following columns:
    - Query
    - Result
    The function should return a pandas DataFrame containing the grid.

    Parameters:
    - index: Index object
    - mode: String indicating the mode. Can be either IDF or Query.
    
    Returns:
    - Pandas DataFrame containing the grid.
    
    """
    if mode == 'IDF':
        # Create DataFrame to hold the inverted index
        df = pd.DataFrame(columns=['Term', 'DF', 'Postings List'])
        # Create an empty list to hold rows
        rows = []
        
        # Retrieve inverted index, term frequencies, and doc IDs from the provided index
        inverted_index = index.posting_lists
        term_frequencies = {term: posting_list.total_frequency for term, posting_list in inverted_index.items()}
        doc_ids = {term: list(posting_list.postings.keys()) for term, posting_list in inverted_index.items()}
        
        # Populate the rows list
        for term, postings_list in inverted_index.items():
            rows.append({
                'Term': term,
                'DF': len(postings_list.postings),
                'Postings List': ", ".join([f"{term_frequencies[term]} {doc_id}" for doc_id in doc_ids[term]])
            })
        # Create a DataFrame from the rows list
        df = pd.DataFrame(rows)
        print("The inverted dataframe was successfully created!")
    elif mode == 'Query':
        # convert the chains to be added to dataframe
        # for key in param:
        #     param[key] = ', '.join(param[key])
        
        # # # Convert dictionary to list of tuples
        # # param_list = [(k, v) for k, v in param.items()]
        # # Create a DataFrame
        # df = pd.DataFrame(list(param.items()), columns=['Query', 'Result'])

        # df.sort_values('Query', inplace=True)
        # print("the query dataframe was sucessfuly created !")
        pass
    
    return df
