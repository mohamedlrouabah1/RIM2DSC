import sys
import nltk
from tqdm import tqdm
from models.IRrun import IRrun
from models.weighting.BM25 import BM25
from models.weighting.SMART_ltc import SMART_ltc
from models.weighting.SMART_ltn import SMART_ltn
from models.weighting.SMART_lnu import SMART_lnu
from utilities.config import NB_RANKING, RECURSION_LIM
from utilities.parser import parse_command_line_arguments
from utilities.utilities import create_or_load_collection, load_queries_from_csv

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
    print("Instanciate IRun class ...", file=sys.stderr)
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
        query = collection.preprocessor._text_preprocessing(query)
        collection.Timer.stop()
        print(f"Query preprocessed in {collection.Timer.get_time(f'query{id:02d}_preprocessing')}")
        print(f"Query preprocessed: {query}")
        print(delimiter)

        print(f"Ranking documents...")
        collection.Timer.start(f"query{id:02d}_ranking")
        ranking = collection.compute_RSV(query)
        collection.Timer.stop()
        print(f"Documents ranked in {collection.Timer.get_time(f'query{id:02d}_ranking')}")
        print(delimiter)

        # we filter overlapping results
        nb_scores = 0
        run_lines = []
        doc_already_return = set()
        run_lines.append(ranking[0])
        j = 1 
        doc_already_return.add(ranking[0][0].split(':')[0])
        while nb_scores < NB_RANKING  and j < len(ranking):
            line_id, line_xpath = run_lines[nb_scores][0].split(':')
            doc_id, xpath = ranking[j][0].split(':')

            # does it overlap with the previous score ?
            if line_id == doc_id  and xpath.find(line_xpath) != -1:
                run_lines[nb_scores] = ranking[j]

            
            # does it not intertwine with a previous result return from the document ?
            elif doc_id not in doc_already_return:
                nb_scores += 1
                if nb_scores < NB_RANKING:
                    run_lines.append(ranking[j])
                    doc_already_return.add(doc_id)

            j+=1
                
        if j < NB_RANKING:
            print(f"Only {j} results for query {id} instead of {NB_RANKING}")


        print(f"Ranking results:")
        for i, (doc_id, score) in enumerate(run_lines[:top_n]):
            print(f"#{i+1} - Document {doc_id} with score {score}")
        print(delimiter)
        print("\n\n")


        # We add the results to the run file
        for i, (doc_id, score) in enumerate(run_lines):
            # xml_path = Document.get_xml_path()
            run.add_result_line(
                query_id=id,
                doc_id=doc_id,
                rank=i+1,
                score=score,
            )

    # Finnally we save the run file
    run.save_run(verbose=True)
    
if __name__ == "__main__":
    sys.setrecursionlimit(RECURSION_LIM)
    # Downloading nltk dependencies
    for dep in  tqdm(["wordnet", "averaged_perceptron_tagger"], desc="Downloading nltk dependencies...", colour="green"):
        nltk.download(dep, quiet=True)
    main()
