from collection_statistics import collection_statistics
from compute_weights import *
from models import *
from document_retrieval import *
def main() -> None:
    """
    Main function of the program.

    """
    # Load the document collection and create the index
    content = load_text_collection(f"{DATA_FOLDER}/{COLLECTION_FILES[0]}")
    index = generate_index_oop(content, mode="basic")
    query = "web ranking scoring algorithm"
    b=0.5
    k1=1.2

    # exercise 1
    # collection_statistics(mode="nltk_stopwords_stemmer", chartname="nltk_stopwords_stemmer")
    # exercise 2
    # collection_statistics(mode="basic", chartname="basic")
    # exercise 3
    # collection_statistics(mode="stemmer", chartname="stemmer")
    
    # Choose the scoring mode: "smart_ltn", "smart_ltc", or "bm25"
    # exercise 5
    # scoring_mode = "smart_ltn"
    # print_ranking(query, scoring_mode="smart_ltn", index, b, k1)
    # exercise 7
    # scoring_mode = "smart_ltc" 
    # print_ranking(query, scoring_mode, index, b, k1)
    # exercise 9
    # scoring_mode = "bm25" 
    # print_ranking(query, scoring_mode="bm25", index, b, k1)

    # plot ranking
    plot_ranking(query, index, b, k1)
   

if __name__ == "__main__":
    main()
