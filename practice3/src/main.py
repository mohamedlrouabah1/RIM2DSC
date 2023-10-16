import argparse
from collection_statistics import collection_statistics
from compute_weights import *
from models import *
from ranking_retrieval import *

def main() -> None:
    # parse the command line arguments
    parser = argparse.ArgumentParser(description="Information Retrieval Exercises")
    parser.add_argument("-e", "--exercise", type=int, help="Exercise number to run (1, 2, 3, 5, 7, 9)")
    args = parser.parse_args()

    # Load the document collection and create the index
    content = load_text_collection(f"{DATA_FOLDER}/{COLLECTION_FILES[0]}")
    index = generate_index_oop(content, mode="basic")
    query = "web ranking scoring algorithm"
    b=0.5
    k1=1.2

    if args.exercise is None:
        print("Please specify an exercise using the --exercise flag.")
        print("Default set to exercice 9.")
        args.exercise = 9

        if args.exercise == 1:
            collection_statistics(mode="nltk_stopwords_stemmer", chartname="nltk_stopwords_stemmer")
        elif args.exercise == 2:
            collection_statistics(mode="basic", chartname="basic")
        elif args.exercise == 3:
            collection_statistics(mode="stemmer", chartname="stemmer")
        elif args.exercise == 5:
            scoring_mode = "smart_ltn"
            print_ranking(query, scoring_mode, index, b, k1)
            plot_ranking(query, index, b, k1)
        elif args.exercise == 7:
            scoring_mode = "smart_ltc"
            print_ranking(query, scoring_mode, index, b, k1)
            plot_ranking(query, index, b, k1)
        elif args.exercise == 9:
            scoring_mode = "bm25"
            print_ranking(query, scoring_mode, index, b, k1)
            plot_ranking(query, index, b, k1)
        else:
            print("Exercise not found. Please choose from exercises 1, 2, 3, 5, 7, or 9.")

if __name__ == "__main__":
    main()
