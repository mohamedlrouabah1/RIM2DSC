from exercise2 import generate_index  
from exercise3 import generate_query
from utils import read_doc,generate_grid
import pandas as pd

def main() -> None:
    ###### Exercise 2 ###### 
    n = 'exo2'
    doc = read_doc('data/documentxml.xml')

    # generate the inverted index, doc freq, and doc_ids
    res = generate_index(doc)
    print(res)
    # Transform list into dataframe 
    df = generate_grid(res,n)
    print(df)


    ###### Exercise 3 ###### 
    n = 'exo3'
    # Read queries from query.txt file
    sample_queries = read_doc('data/query_sample.txt').strip().split('\n')
    print(sample_queries)

    res2 = generate_query(sample_queries,res)
    print(res2)
    dq = generate_grid(res2, n)
    print(dq)

    ##### Export files ##### 
    # Export DataFrame to CSV
    df.to_csv('data/exo2InvertedIndex.csv', index=False)
    # Export DataFrame to CSV
    dq.to_csv('data/exo3Query.csv', index=False)

if __name__ == "__main__":
    main()