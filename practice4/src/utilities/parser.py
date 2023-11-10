import argparse

def parse_command_line_arguments() -> argparse.Namespace:
    """
    >main.py -e N
    N: exercise number to run (1, 2, 3, 5, 7, 9)
        default value: 9
    """
    parser = argparse.ArgumentParser(
        prog="Information Retrieval Practice",
        description="Information Retrieval Exercises"
        )
    
    parser.add_argument(
        "-i", "--generate-index",
        action="store_true", 
        help="Force the generation of a new index, given the preprocess parameters given [tokenizer, stopword, stemmer, lemmer]."
        )
    
    # ======= Preprocessing arguments =======
    
    parser.add_argument(
        "-t", "--tokenizer",
        choices=["regex", "nltk"],
        default="nltk",
        help="Tokenizer to use for preprocessing."
        )
    
    parser.add_argument(
        "-s", "--stopword",
        action="store_true",
        help="To use stopword removal for preprocessing."
        )
    
    parser.add_argument(
        "-l", "--lemmer",
        action="store_true",
        help="To use lemmatization for preprocessing."
        )
    
    parser.add_argument(
        "-m", "--stemmer",
        choices=["None", "porter", "snowball"],
        default="porter",
        help="Stemmer to use for preprocessing."
        )
    
    parser.add_argument(
        "-p", "--plot",
        action="store_true",
        help="Plot the collection statistics, only if the index is computed with -i."
        )
    
    parser.add_argument(
        "-pc", "--parallel-computing",
        action="store_true",
        help="Use parallel computing for preprocessing and indexing."
        )
    
    # ======= Ranking arguments =======

    parser.add_argument(
        "-r", "--ranking",
        choices=["bm25", "smart_ltn", "smart_ltc"],
        default="bm25",
        help="Ranking algorithm to use."
        )

    parser.add_argument(
        "-b", "--b",
        type=float,
        default=0.5,
        help="BM25 parameter b. It has no effect on other ranking algorithms."
        )
    
    parser.add_argument(
        "-k", "--k1",
        type=float,
        default=1.2,
        help="BM25 parameter k1. It has no effect on other ranking algorithms."
        )
    
    parser.add_argument(
        "-n", "--top-n",
        type=int,
        default=10,
        help="Number of documents to retrieve."
        )
    
    parser.add_argument(
        "queries_file_path",
        type=str,
        help="Path to a csv file containing the queries and their ids."
        )

    parser.add_argument(
        "-g", "--gradient-descent",
        choices=["k1", "b"],
        default=None,
        help="Perform gradient descent on the given parameter."
        )

    return parser.parse_args()
