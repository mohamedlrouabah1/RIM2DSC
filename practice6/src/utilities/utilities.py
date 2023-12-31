import os
from sys import stderr
from utilities.config import SAVE_FOLDER, COLLECTION_NAME, DATA_PRACTICE_5
from models.txt.TextCollection import TextCollection
from models.txt.TextIndexer import TextIndexer
from models.txt.TextPreprocessor import TextPreprocessor
from models.xml.XMLCollection import XMLCollection
from models.xml.XMLIndexer import XMLIndexer
from models.xml.XMLPreprocessor import XMLPreprocessor
from models.IRrun import IRrun


def create_or_load_collection(args, type="xml", save=True) -> TextCollection:
    """
    Check if the index based on the given arguments already exists.
    If it does, load it. Otherwise, create it.
    """
    # First create the path to the save index file
    index_path = f"{SAVE_FOLDER}/index_" 
    index_path += "regex_" if args.tokenizer == "regex" else "nltk_" 
    index_path += "stop_" if args.stopword else "nostop_" 
    index_path += "lem_" if args.lemmer else "nolem_"

    if args.stemmer == "None":
        index_path += "nostem_"
    else:
        index_path += "snow_" if args.stemmer == "snowball" else "porter_"  

    index_path += COLLECTION_NAME + ".pkl"

    is_existing_index = os.path.isfile(index_path)
    if is_existing_index:
        print(f"Index file {index_path} already exists.", file=stderr)
    else:
        print(f"Index file {index_path} does not exist.", file=stderr)
    
    # Second we create the TextPreProcessor object
    if type == "xml":
        preprocessor = XMLPreprocessor(
            exclude_stopwords=args.stopword,
            exclude_digits=args.stopword,
            tokenizer=args.tokenizer,
            lemmer=args.lemmer,
            stemmer=args.stemmer
        )
    else:
       preprocessor = TextPreprocessor(
            exclude_stopwords=args.stopword,
            exclude_digits=args.stopword,
            tokenizer=args.tokenizer,
            lemmer=args.lemmer,
            stemmer=args.stemmer
        )

    # Finnally Do we need to compute the indexed Collection ?
    if args.generate_index or not is_existing_index:
        if type == "xml":
            index = XMLIndexer()
            collection = XMLCollection(
                path=DATA_PRACTICE_5,
                indexer=index,
                preprocessor=preprocessor,
                use_parallel_computing=args.parallel_computing if args.parallel_computing else False
            )
        else:
            index = TextIndexer()
            collection = TextCollection(
                path=DATA_PRACTICE_5,
                indexer=index,
                preprocessor=preprocessor,
                use_parallel_computing=args.parallel_computing if args.parallel_computing else False
            )
        raw_collection = collection.load()
        collection.preprocess(raw_collection)
        collection.index()
        collection.compute_stats()
        if save:
            collection.serialize(index_path)
    
        collection.index_path = index_path

    else:
        if type == "xml":
            print(f"deserialize {index_path}", file=stderr)
            collection = XMLCollection.deserialize(index_path)
        else:
            collection = TextCollection.deserialize(index_path)
        
        collection.preprocessor =preprocessor
    
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


def launch_run(collection:XMLCollection, queries:list, file_name, a_ranking, a_params) -> None:
    # get info from collection save file name
    tmp = file_name.split('_')
    a_stopword = tmp[2]
    a_stemmer = tmp[5]
    
    # To create run result files
    print("Instanciate IRun class ...", file=stderr)
    run = IRrun(a_ranking, a_stopword, a_stemmer, a_params)
    run.ranking(collection, queries)
    run.save_run(verbose=True)
