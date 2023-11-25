import glob
from multiprocessing import Pool
from pathlib import Path
import nltk
import os
from numpy import gradient
from regex import D
from tqdm import tqdm
import xml
from models.Collection import Collection
from models.Indexer import Indexer
from models.IRrun import IRrun
from models.TextPreprocessor import TextPreprocessor
from models.weighting.BM25 import BM25
from models.weighting.SMART_ltc import SMART_ltc
from models.weighting.SMART_ltn import SMART_ltn
from models.Document import Document
from utilities.config import DATA_FOLDER, COLLECTION_NAME, SAVE_FOLDER, NB_RANKING
from utilities.parser import parse_command_line_arguments


def get_index_path(args) -> str:
    index_path = f"{SAVE_FOLDER}/index_"
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
    # # Process program's arguments
    args = parse_command_line_arguments()    
    
    # First create the path to the save index file
    index_path = get_index_path(args)    
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

    # xml_path = "../../data/XML-Zip/XML.zip"
    xml_path="../../data/XML-Coll-withSem/"
    # print(xml_files)
    # print(len(xml_files))
    # Finnally Do we need to compute the indexed Collection ?
    if args.generate_index or not is_existing_index:
        # pbar = tqdm(total=len(xml_files), desc="browse XML articles", unit="file")
        index = Indexer()
        collection = Collection(
            path=xml_path,
            indexer=index,
            preprocessor=text_preprocessor,
            use_parallel_computing=args.parallel_computing if args.parallel_computing else False
        )
        collection.load_and_preprocess()
        collection.compute_index() # type: ignore
        collection.compute_statistics() # type: ignore
        collection.serialize(index_path) # type: ignore
    else:
        collection = Collection.deserialize(index_path)
        collection.preprocessor = text_preprocessor #type: ignore
    
    print(collection) # type: ignore
    if args.plot:
        collection.plot_statistics() # type: ignore

    # We create the ranking function
    # if args.ranking == "smart_ltn":
    #     ranking_function = SMART_ltn(N=len(collection))
    # elif args.ranking == "smart_ltc":
    #     ranking_function = SMART_ltc(N=len(collection))
    # else:
    #     ranking_function = BM25(
    #         N=len(collection),
    #         avdl=collection.get_avdl(), 
    #         b=args.b, k1=args.k1
    #         )
    # collection.information_retriever = ranking_function


    # # Now we can use the index and the preprocessor to do the queries
    # csv_queries = args.queries_file_path
    # try:
    #     queries = [line.strip().split(',') for line in open(csv_queries, "r")]
    # except FileNotFoundError:
    #     print(f"File {csv_queries} not found.")
    #     return
    

    # # To create the run file
    # run = IRrun(
    #     weighting_function=args.ranking,
    #     stop=args.stopword,
    #     stem=args.stemmer,
    #     params=[f"k{args.k1}", f"b{args.b}"],
    # )

    # # for the display
    # delimiter = "-" * 80
    # top_n = args.top_n
    
    # for id, query in queries:
    #     id = int(id)
    #     print(f"Query: {query}")
    #     collection.Timer.start(f"query{id:02d}_preprocessing")
    #     query = collection.preprocessor.doc_preprocessing(query)
    #     collection.Timer.stop()
    #     print(f"Query preprocessed in {collection.Timer.get_time(f'query{id:02d}_preprocessing')}")
    #     print(f"Query preprocessed: {query}")
    #     print(delimiter)

    #     print(f"Ranking documents...")
    #     collection.Timer.start(f"query{id:02d}_ranking")
    #     ranking = collection.RSV(query)
    #     collection.Timer.stop()
    #     print(f"Documents ranked in {collection.Timer.get_time(f'query{id:02d}_ranking')}")
    #     print(delimiter)

    #     print(f"Ranking results:")
    #     for i, (doc_id, score) in enumerate(ranking[:top_n]):
    #         print(f"#{i+1} - Document {doc_id} with score {score}")
    #     print(delimiter)
    #     print("\n\n")

    #     # We add the results to the run file
    #     for i, (doc_id, score) in enumerate(ranking[:NB_RANKING]):
    #         # xml_path = Document.get_xml_path()
    #         run.add_result_line(
    #             query_id=id,
    #             doc_id=doc_id,
    #             rank=i+1,
    #             score=score,
    #         )
    # # Finnally we save the run filea
    # run.save_run(verbose=True)




if __name__ == "__main__":
    # Downloading nltk dependencies
    for dep in  tqdm(["wordnet", "averaged_perceptron_tagger"], desc="Downloading nltk dependencies...", colour="green"):
        nltk.download(dep, quiet=True)
    main()
