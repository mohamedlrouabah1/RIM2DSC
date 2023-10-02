import pandas as pd
import gzip
import time
from generate_index import generate_index_oop
from utilities.time_utility import convert_time_from_ns_to_s

DATA_FOLDER="../data"
RENDU_FOLDER="../rendus"
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

def index_files_and_measure_time(filenames: list, print_index: bool = False) -> list:
    """
    This function takes in a list of filenames and indexes each file. It then measures 
    the time it takes to index each file and returns a list of these times.
    
    Parameters:
    - filenames: List of file names to be indexed.
    - print_index: Boolean flag indicating whether the index should be printed or not. 
      By default, it is set to False.
    
    Returns:
    - List of time durations (in seconds) for indexing each file.
    """
    
    # Initialize an empty list to store the time taken for indexing each file.
    times = []

    # Loop over each file in the filenames list.
    for file in filenames:
        # Read the content of the file using the `load_text_collection` function.
        doc = load_text_collection(f"{DATA_FOLDER}/{file}")
        
        # Record the start time just before indexing starts.
        start_time = time.perf_counter_ns()

        # Generate the index for the current document without stemmer or stopword.
        index = generate_index_oop(doc, 3)  
        
        # Record the end time just after indexing completes.
        end_time = time.perf_counter_ns()

        # Calculate the total time taken to index the file.
        indexing_time_in_ns = end_time - start_time
        index.indexing_time_in_ns = indexing_time_in_ns
        indexing_time_in_s = convert_time_from_ns_to_s(indexing_time_in_ns)

        # Print out a message indicating how long it took to index the current file.
        # print(f"Indexed {file} in {indexing_time_in_s:.2f} seconds.")
        
        # If the print_index flag is True and the size of the document is less than 
        # 1 MB, then print the index.
        if print_index and len(doc) < 1e6:
            print(index)
        
        # Append the time taken to index the current file to the `times` list.
        times.append(indexing_time_in_s)
    
    # Return the list of indexing times.
    return times

