import nltk
from tqdm import tqdm
from models.IRrun import IRrun
from models.weighting.BM25 import BM25
from models.weighting.SMART_ltc import SMART_ltc
from models.weighting.SMART_ltn import SMART_ltn
from utilities.config import NB_RANKING
from utilities.parser import parse_command_line_arguments
from utilities.utilities import create_or_load_collection, load_queries_from_csv

def main() -> None:
    # Process program's arguments
    args = parse_command_line_arguments()    
    
    # Create/Load the Collection
    collection = create_or_load_collection(args)
    if args.plot: collection.plot_statistics()

    # We create the ranking function
    params=[]
    if args.ranking == "smart_ltn":
        ranking_function = SMART_ltn(N=len(collection))
    elif args.ranking == "smart_ltc":
        ranking_function = SMART_ltc(N=len(collection))
    else:
        ranking_function = BM25(
            N=len(collection),
            avdl=collection.get_avdl(), 
            b=args.b, k1=args.k1
            )
        params = [f"k{args.k1}", f"b{args.b}"]
    collection.information_retriever = ranking_function


    # Now we can use the index and the preprocessor to do the queries
    queries = load_queries_from_csv(args.queries_file_path)
    

    # To create run result files
    run = IRrun(
        weighting_function=args.ranking,
        stop=args.stopword,
        stem=args.stemmer,
        params=params,
    )

    # for the display
    delimiter = "-" * 80
    top_n = args.top_n
    
    for id, query in queries:
        id = int(id)
        print(f"Query: {query}")
        collection.Timer.start(f"query{id:02d}_preprocessing")
        query = collection.preprocessor.doc_preprocessing(query)
        collection.Timer.stop()
        print(f"Query preprocessed in {collection.Timer.get_time(f'query{id:02d}_preprocessing')}")
        print(f"Query preprocessed: {query}")
        print(delimiter)

        print(f"Ranking documents...")
        collection.Timer.start(f"query{id:02d}_ranking")
        ranking = collection.RSV(query)
        collection.Timer.stop()
        print(f"Documents ranked in {collection.Timer.get_time(f'query{id:02d}_ranking')}")
        print(delimiter)

        print(f"Ranking results:")
        for i, (doc_id, score) in enumerate(ranking[:top_n]):
            print(f"#{i+1} - Document {doc_id} with score {score}")
        print(delimiter)
        print("\n\n")

        # We add the results to the run file
        for i, (doc_id, score) in enumerate(ranking[:NB_RANKING]):
            # xml_path = Document.get_xml_path()
            run.add_result_line(
                query_id=id,
                doc_id=doc_id,
                rank=i+1,
                score=score,
            )


    # Finnally we save the run filea
    run.save_run(verbose=True)




if __name__ == "__main__":
    # Downloading nltk dependencies
    for dep in  tqdm(["wordnet", "averaged_perceptron_tagger"], desc="Downloading nltk dependencies...", colour="green"):
        nltk.download(dep, quiet=True)
    main()
