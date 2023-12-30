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
                launch_run(collection, queries, index_path, "smart_ltn", [])

                ranking_function = SMART_ltc(N=len(collection))
                collection.information_retriever = ranking_function
                launch_run(collection, queries, index_path, "smart_ltc", [])

                for slope in [0.1, 0.2, 0.3, 0.4, 0.5]:
                    ranking_function = SMART_lnu(N=len(collection), slope=slope)
                    collection.information_retriever = ranking_function
                    launch_run(collection, queries, index_path, "smart_lnu", [f"slope{slope}"])

                
                for k1 in [1.2, 1.7, 2.2, 3.7]:
                    for b in [0.5, 0.75, 0.9]:
                        ranking_function = BM25(
                            N=len(collection),
                            avdl=collection.get_avdl(), 
                            b=b, k1=k1
                            )
                        collection.information_retriever = ranking_function
                        launch_run(collection, queries, index_path, "bm25", [f"k{k1}", f"b{b}"])




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


if __name__ == "__main__":
    main()