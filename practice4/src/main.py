import nltk
import os
from models.Collection import Collection
from models.Indexer import Indexer
from models.TextPreprocessor import TextPreprocessor
from models.weighting.BM25 import BM25
from models.weighting.SMART_ltc import SMART_ltc
from models.weighting.SMART_ltn import SMART_ltn
from utilities.config import DATA_FOLDER, COLLECTION_FILES, COLLECTION_NAME
from utilities.parser import parse_command_line_arguments


def get_index_path(args) -> str:
    index_path = "index_"
    index_path += "regex_" if args.tokenizer == "regex" else "nltk_"
    index_path += "stop_" if args.stopword else "nostop_"
    index_path += "lem_" if args.lemmer else "nolem_"

    if args.stemmer is None:
        index_path += "nostem_"
    else:
        index_path += "snow_" if args.stemmer == "snowball" else "porter_"  

    index_path += COLLECTION_NAME + ".pkl"
    return index_path


def main() -> None:
    # Process program's arguments
    args = parse_command_line_arguments()

    # First create the path to the save index file
    index_path = get_index_path(args)    
    is_existing_index = os.path.isfile(index_path)

    # Second we create the TextPreProcessor object
    text_preprocessor = TextPreprocessor(
        exclude_stopwords=args.stopword,
        exclude_digits=args.stopword,
        tokenizer=args.tokenizer,
        lemmer=args.lemmer,
        stemmer=args.stemmer
    )

    # Third we create the ranking function
    if args.ranking == "smart_ltn":
        ranking_function = SMART_ltn()
    elif args.ranking == "smart_ltc":
        ranking_function = SMART_ltc()
    else:
        ranking_function = BM25(b=args.b, k1=args.k1)

    # Finnally Do we need to compute the indexed Collection ?
    if args.generate_index or not is_existing_index:
        index = Indexer()
        collection = Collection(
            path=os.path.join(DATA_FOLDER, COLLECTION_NAME),
            indexer=index,
            preprocessor=text_preprocessor,
            ranking_function=ranking_function,
        )
        collection.load_and_preprocess()
        collection.compute_index()
        index.serialize(index_path)
        collection.compute_statistics()
        print(collection)
        if args.plot:
            collection.plot_statistics()

    else:
        collection = Collection.deserialize(index_path)


    # Now we can use the index and the preprocessor to do the queries
    queries = args.queries
    delimiter = "-" * 80
    k = args.top_n
    for id, query in enumerate(queries):
        print(f"Query: {query}")
        collection.Timer.start(f"query{id:02d}_preprocessing")
        query = collection.text_preprocessor.doc_preprocessing(query)
        collection.Timer.stop(f"query{id:02d}_preprocessing")
        print(f"Query preprocessed in {collection.Timer.get_time(f'query{id:02d}_preprocessing')} seconds.")
        print(f"Query preprocessed: {query}")
        print(delimiter)

        print(f"Ranking documents...")
        collection.Timer.start(f"query{id:02d}_ranking")
        ranking = collection.information_retriever.RSV(query)
        collection.Timer.stop(f"query{id:02d}_ranking")
        print(f"Documents ranked in {collection.Timer.get_time(f'query{id:02d}_ranking')} seconds.")
        print(delimiter)

        print(f"Ranking results:")
        for i, (doc_id, score) in enumerate(ranking):
            print(f"#{i+1} - Document {doc_id} with score {score}")
        print(delimiter)
        print("\n\n")



if __name__ == "__main__":
    # Downloading nltk dependencies
    for dep in  ['stopwords', 'wordnet', 'punkt']:
        nltk.download(dep)
    main()
