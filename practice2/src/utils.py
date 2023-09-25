import pandas as pd
import gzip
import time
import generate_index
def read_doc(path) -> str:
    """Read the document collection from a file. Handles both regular and gzipped files."""
    if path.endswith('.gz'):
        with gzip.open(path, 'rt', encoding='utf-8') as f:
            document_collection_str = f.read()
    else:
        with open(path, 'r') as f:
            document_collection_str = f.read()
    return document_collection_str

def generate_grid(param,n) -> pd.DataFrame:
    if (n == 'exo2'):
        # Create DataFrame to hold the inverted index
        df = pd.DataFrame(columns=['Term', 'DF', 'Postings List'])
        # Create an empty list to hold rows
        rows = []
        # Populate the rows list
        # param[0] = indexInverted
        # param[1] = tf
        # param[2] = doc_ids
        for term, postings_list in param[0].items():
            rows.append({
                'Term': term,
                'DF': len(postings_list),
                'Postings List': ", ".join([f"{param[1][term][doc_id]} {doc_id}" for doc_id in postings_list])
            })
        # Create a DataFrame from the rows list
        df = pd.DataFrame(rows)
        print("the inverted dataframe was sucessfuly created !")
    elif (n == 'exo3'): 
        # convert the chains to be added to dataframe
        for key in param:
            param[key] = ', '.join(param[key])
        
        # # Convert dictionary to list of tuples
        # param_list = [(k, v) for k, v in param.items()]
        # Create a DataFrame
        df = pd.DataFrame(list(param.items()), columns=['Query', 'Result'])

        df.sort_values('Query', inplace=True)
        print("the query dataframe was sucessfuly created !")
    
    
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
        # Read the content of the file using the `read_doc` function.
        doc = read_doc(f"D:/M2/RIM2DSC/TP/practice2/data/{file}")
        
        # Record the start time just before indexing starts.
        start_time = time.time()

        # Generate the index for the current document.
        index = generate_index.generate_index(doc)  
        
        # Record the end time just after indexing completes.
        end_time = time.time()

        # Calculate the total time taken to index the file.
        indexing_time = end_time - start_time

        # Print out a message indicating how long it took to index the current file.
        print(f"Indexed {file} in {indexing_time:.2f} seconds.")
        
        # If the print_index flag is True and the size of the document is less than 
        # 1 MB, then print the index.
        if print_index and len(doc) < 1e6:
            print(index)
        
        # Append the time taken to index the current file to the `times` list.
        times.append(indexing_time)
    
    # Return the list of indexing times.
    return times