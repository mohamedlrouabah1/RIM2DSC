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
        choices=["basic", "nltk"],
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
        choices=["porter", "snowball"],
        default="porter",
        help="Stemmer to use for preprocessing."
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
        help="BM25 parameter b. It has no effect on pther ranking algorithms."
        )
    
    parser.add_argument(
        "-k", "--k1",
        type=float,
        default=1.2,
        help="BM25 parameter k1. It has no effect on pther ranking algorithms."
        )
    
    return parser.parse_args()



def validate_command_line_arguments(args: argparse.Namespace) -> argparse.Namespace:
    raise NotImplementedError("TODO: update this fuction accordingly to the new arguments.")
    if args.exercise is None:
        print("Please specify an exercise using the --exercise flag with value 1, 2, 3, 5, 7, or 9.")
        print("Default set to exercice 9.")
        args.exercise = 9

    if args.exercise not in [1, 2, 3, 5, 7, 9]:
        print("Exercise not found. Please choose from exercises 1, 2, 3, 5, 7, or 9.")
        return None

    return args