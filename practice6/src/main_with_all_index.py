import os
from sys import stderr
from tqdm import tqdm

from models.xml.XMLCollection import XMLCollection
from models.xml.XMLDocument import XMLDocument
from models.IRrun import IRrun
from models.weighting.BM25 import BM25
from models.weighting.SMART_ltc import SMART_ltc
from models.weighting.SMART_ltn import SMART_ltn
from models.weighting.SMART_lnu import SMART_lnu
from utilities.utilities import load_queries_from_csv, create_or_load_collection
from utilities.config import NB_RANKING

DIR_SAVE='../../saves'
DIR_Q='../queries.csv'

class ARGS :
    def __init__(self) -> None:
        pass


def main():
    args = ARGS()
    args.tokenizer = "nltk"
    args.lemmer = True
    args.parallel_computing = False
    args.generate_index = True


    for granularity in [["article", "title", "bdy", "p"]]: # ["element"],
        XMLDocument.granularity = granularity
        print(f"granularity: {granularity}")
        for stopword in [True]: # False
            args.stopword = stopword

            for stemmer in ["porter"]: # "None",
                args.stemmer = stemmer

                collection = None # free memory
                collection = create_or_load_collection(args, type="xml", save=False)
                index_path = f"{DIR_SAVE}/index_regex_{stopword}_nltk_{stopword}_{stemmer}_collection5.pkl"

                print("Loading queries...", file=stderr)
                queries = load_queries_from_csv(DIR_Q)

                # for each weighting function
                ranking_function = SMART_ltn(N=len(collection))
                collection.information_retriever = ranking_function
                rank(collection, queries, index_path, "smart_ltn", [])

                ranking_function = SMART_ltc(N=len(collection))
                collection.information_retriever = ranking_function
                rank(collection, queries, index_path, "smart_ltc", [])

                for slope in [0.1, 0.2, 0.3, 0.4, 0.5]:
                    ranking_function = SMART_lnu(N=len(collection), slope=slope)
                    collection.information_retriever = ranking_function
                    rank(collection, queries, index_path, "smart_lnu", [f"slope{slope}"])

                
                for k1 in [1.2, 1.7, 2.2, 3.7]:
                    for b in [0.5, 0.75, 0.9]:
                        ranking_function = BM25(
                            N=len(collection),
                            avdl=collection.get_avdl(), 
                            b=b, k1=k1
                            )
                        collection.information_retriever = ranking_function
                        rank(collection, queries, index_path, "bm25", [f"k{k1}", f"b{b}"])




def rank(collection:XMLCollection, queries:list, file_name, a_ranking, a_params) -> None:
    # get info from collection save file name
    tmp = file_name.split('_')
    a_stopword = tmp[2]
    a_stemmer = tmp[5]
    
    # To create run result files
    print("Instanciate IRun class ...", file=stderr)
    run = IRrun(
        weighting_function=a_ranking,
        stop=a_stopword,
        stem=a_stemmer,
        params=a_params,
    )

    # for the display
    delimiter = "-" * 80
    top_n = 10
    
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


        #############
        #OVERLAPPING#
        #############
        # we filter overlapping results sorting by doc_id
        nb_scores, j, n = 0, 1, len(ranking)
        run_lines = [ranking[0]]

        while nb_scores < n  and j < n:
            line_id, line_xpath = run_lines[nb_scores][0].split(':')
            doc_id, xpath = ranking[j][0].split(':')

            # does it overlap with the previous score ?
            if line_id == doc_id  and xpath.find(line_xpath) != -1:
                run_lines[nb_scores] = ranking[j]

            j+=1
                


        #############
        #EXTRACTION #
        #############
        # we sort by score and then extract NB_RANKING results
        run_lines.sort(key=lambda x: x[1], reverse=True)
        run_lines = run_lines[:NB_RANKING]
        

        #############
        #INTERTWINED#
        #############
        # we sort by doc_id the extracted NB_RANKING best result
        run_lines.sort(key=lambda x: x[0])


        #############
        #DISPLAY    #
        #############
        if j < NB_RANKING:
            print(f"Only {j} results for query {id} instead of {NB_RANKING}")
        print(f"Ranking results:")
        for i, (doc_id, score) in enumerate(run_lines[:top_n]):
            print(f"#{i+1} - Document {doc_id} with score {score}")
        print(delimiter)
        print("\n\n")


        # We add the results to the run file
        # We modify the score according to INEX Run specification that need
        # to have result with decresing scores.
        for i, (doc_id, _) in enumerate(run_lines):
            run.add_result_line(
                query_id=id,
                doc_id=doc_id,
                rank=i+1,
                score=NB_RANKING - i,
            )

    # Finnally we save the run file
    run.save_run(verbose=True)


if __name__ == "__main__":
    main()