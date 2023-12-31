import sys
import nltk
from tqdm import tqdm
from models.weighting.BM25 import BM25
from models.weighting.SMART_ltc import SMART_ltc
from models.weighting.SMART_ltn import SMART_ltn
from models.weighting.SMART_lnu import SMART_lnu
from utilities.config import RECURSION_LIM
from utilities.parser import parse_command_line_arguments
from utilities.utilities import create_or_load_collection, load_queries_from_csv, launch_run

def main() -> None:
    # Process program's arguments
    args = parse_command_line_arguments()    
    
    # Create/Load the Collection
    collection = create_or_load_collection(args)
    if args.plot: collection.plot_statistics()

    # We create the ranking function
    print("Creating ranking function...", file=sys.stderr)
    params=[]
    if args.ranking == "smart_ltn":
        ranking_function = SMART_ltn(N=len(collection))
    elif args.ranking == "smart_ltc":
        ranking_function = SMART_ltc(N=len(collection))
    elif args.ranking == "smart_lnu":
        ranking_function = SMART_lnu(N=len(collection), slope=args.slope)
        params = [f"slope{args.slope}"]
    else:
        ranking_function = BM25(
            N=len(collection),
            avdl=collection.get_avdl(), 
            b=args.b, k1=args.k1
            )
        params = [f"k{args.k1}", f"b{args.b}"]
    collection.information_retriever = ranking_function


    # Now we can use the index and the preprocessor to do the queries
    print("Loading queries...", file=sys.stderr)
    queries = load_queries_from_csv(args.queries_file_path)
    
    # To create run result files
    launch_run(collection, queries, args.index_path, args.ranking, params)
   
    
if __name__ == "__main__":
    sys.setrecursionlimit(RECURSION_LIM)
    # Downloading nltk dependencies
    for dep in  tqdm(["wordnet", "averaged_perceptron_tagger"], desc="Downloading nltk dependencies...", colour="green"):
        nltk.download(dep, quiet=True)
    main()
