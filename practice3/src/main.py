from collection_statistics import collection_statistics
from compute_weights import *

def main() -> None:
    """
    Main function of the program.

    """
    # exercise 1
    # collection_statistics(mode="nltk_stopwords_stemmer", chartname="nltk_stopwords_stemmer")
    # exercise 2
    # collection_statistics(mode="basic", chartname="basic")
    # exercise 3
    # collection_statistics(mode="stemmer", chartname="stemmer")
    # exercise 4
    # smart_ltn()
    smart_ltc()
    # smart_bm25()
if __name__ == "__main__":
    main()
