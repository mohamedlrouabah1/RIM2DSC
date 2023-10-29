import argparse
from collection_statistics import collection_statistics
from ranking_retrieval import print_ranking, plot_ranking
from utilities.config import DATA_FOLDER, COLLECTION_FILES
from utilities.parser import parse_command_line_arguments, validate_command_line_arguments
from utilities.utils import load_text_collection, generate_index_oop


def run_exercice(n: int, index, query, b=0.5, k1=1.2) -> None:
    if n == 1:
        collection_statistics(mode="nltk_stopwords_stemmer", chartname="nltk_stopwords_stemmer")
    elif n == 2:
        print("Exercice 2:")
        collection_statistics(mode="basic", chartname="basic")
    elif n == 3:
        collection_statistics(mode="stemmer", chartname="stemmer")
    elif n == 5:
        scoring_mode = "smart_ltn"
        print_ranking(query, scoring_mode, index, b, k1)
        plot_ranking(query, index, b, k1)
    elif n == 7:
        scoring_mode = "smart_ltc"
        print_ranking(query, scoring_mode, index, b, k1)
        plot_ranking(query, index, b, k1)
        scoring_mode = "bm25"
        print_ranking(query, scoring_mode, index, b, k1)
        plot_ranking(query, index, b, k1)
    # elif n == 9:
        # scoring_mode = "bm25"
        # print_ranking(query, scoring_mode, index, b, k1)
        # plot_ranking(query, index, b, k1)
    else:
        print("Exercise not found. Please choose from exercises 1, 2, 3, 5, 7, or 9.")




def main() -> None:
    # Process program's arguments
    args = parse_command_line_arguments()
    args = validate_command_line_arguments(args)
    if args is None: return

    # Load the document collection and create the index
    content = load_text_collection(f"{DATA_FOLDER}/{COLLECTION_FILES[0]}")
    index = generate_index_oop(content, mode="nltk_stopwords_stemmer")
    query = "web ranking scoring algorithm"

    # Run the exercise
    run_exercice(args.exercise, index, query)
    # run_exercice(args.exercise)


if __name__ == "__main__":
    main()
