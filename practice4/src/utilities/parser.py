import argparse

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