import pandas as pd


def read_doc(path) -> str:
    """Read the document collection from a file"""
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