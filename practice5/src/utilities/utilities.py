import os
from sys import stderr
from utilities.config import SAVE_FOLDER, COLLECTION_NAME, DATA_PRACTICE_5
from models.Collection import Collection
from models.Indexer import Indexer
from models.TextPreprocessor import TextPreprocessor

def create_or_load_collection(args) -> Collection:
    """
    Check if the index based on the given arguments already exists.
    If it does, load it. Otherwise, create it.
    """
    # First create the path to the save index file
    index_path = f"{SAVE_FOLDER}/index_" 
    index_path += "regex_" if args.tokenizer == "regex" else "nltk_" 
    index_path += "stop_" if args.stopword else "nostop_" 
    index_path += "lem_" if args.lemmer else "nolem_"

    if args.stemmer is None:
        index_path += "nostem_"
    else:
        index_path += "snow_" if args.stemmer == "snowball" else "porter_"  

    index_path += COLLECTION_NAME + ".pkl"

    is_existing_index = os.path.isfile(index_path)
    if is_existing_index:
        print(f"Index file {index_path} already exists.")
    else:
        print(f"Index file {index_path} does not exist.")
    
    # Second we create the TextPreProcessor object
    text_preprocessor = TextPreprocessor(
        exclude_stopwords=args.stopword,
        exclude_digits=args.stopword,
        tokenizer=args.tokenizer,
        lemmer=args.lemmer,
        stemmer=args.stemmer
    )

    # Finnally Do we need to compute the indexed Collection ?
    if args.generate_index or not is_existing_index:
        # pbar = tqdm(total=len(xml_files), desc="browse XML articles", unit="file")
        index = Indexer()
        collection = Collection(
            path=DATA_PRACTICE_5,
            indexer=index,
            preprocessor=text_preprocessor,
            use_parallel_computing=args.parallel_computing if args.parallel_computing else False
        )
        raw_collection = collection.load()
        collection.preprocess(raw_collection)
        collection.index()
        collection.compute_stats()
        collection.serialize(index_path)
    else:
        collection = Collection.deserialize(index_path)
        collection.preprocessor = text_preprocessor
    
    print(collection, file=stderr)

    return collection


def load_queries_from_csv(path:str) -> list:
    """
    Load the queries from a csv file.
    """
    queries = []

    try:
       with open(path, "r") as file:
            queries = [line.strip().split(',') for line in file]
            
    except FileNotFoundError:
        print(f"File {path} not found.", file=stderr)

    return queries