from exercise2 import generate_index  
from exercise3 import generate_query
from src.utils import load_text_collection,generate_grid

def main() -> None:
    ###### Exercise 2 ###### 
    n = 'exo2'
    doc = load_text_collection('data/documentxml.xml')

    # generate the inverted index, doc freq, and doc_ids
    res = generate_index(doc)
    print(res)
    # Transform list into dataframe 
    df = generate_grid(res,n)
    print(df)


    ###### Exercise 3 ###### 
    n = 'exo3'
    # Read queries from query.txt file
    sample_queries = load_text_collection('data/query_sample.txt').strip().split('\n')
    print(sample_queries)

    res2 = generate_query(sample_queries,res)
    print(res2)
    dq = generate_grid(res2, n)
    print(dq)

    ##### Export files ##### 
    # Export DataFrame to CSV
    df.to_csv('data/output_ex2.csv', index=False)
    # Export DataFrame to CSV
    dq.to_csv('data/output_ex3.csv', index=False)

if __name__ == "__main__":
    main()