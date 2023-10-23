import argparse
from collection_statistics import collection_statistics
from compute_weights import *
from models import *
from ranking_retrieval import *

def parse_command_line_arguments() -> argparse.Namespace:
    """
    >main.py -e N
    N: exercise number to run (1, 2, 3, 5, 7, 9)
        default value: 9
    """
    parser = argparse.ArgumentParser(
        prog="Information Retrieval Practice",
        description="Information Retrieval Exercises")
    parser.add_argument(
        "-e", "--exercise", 
        type=int, 
        help="Exercise number to run (1, 2, 3, 5, 7, 9)")
    
    return parser.parse_args()


def validate_command_line_arguments(args: argparse.Namespace) -> argparse.Namespace:
    if args.exercise is None:
        print("Please specify an exercise using the --exercise flag with value 1, 2, 3, 5, 7, or 9.")
        print("Default set to exercice 9.")
        args.exercise = 9

    if args.exercise not in [1, 2, 3, 5, 7, 9]:
        print("Exercise not found. Please choose from exercises 1, 2, 3, 5, 7, or 9.")
        return None

    return args


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
    elif n == 9:
        scoring_mode = "bm25"
        print_ranking(query, scoring_mode, index, b, k1)
        plot_ranking(query, index, b, k1)
    else:
        print("Exercise not found. Please choose from exercises 1, 2, 3, 5, 7, or 9.")




def main() -> None:
    # Process program's arguments
    args = parse_command_line_arguments()
    args = validate_command_line_arguments(args)
    if args is None: return

    # Load the document collection and create the index
    content = load_text_collection(f"{DATA_FOLDER}/{COLLECTION_FILES[0]}")
    index = generate_index_oop(content, mode="basic")
    query = "web ranking scoring algorithm"

    # Run the exercise
    run_exercice(args.exercise, index, query)


if __name__ == "__main__":
    main()
