from sys import stderr

from models.xml.XMLDocument import XMLDocument
from models.weighting.BM25 import BM25
from models.weighting.BM25Fw import BM25Fw
from models.weighting.BM25Fr import BM25Fr
from models.weighting.SMART_ltc import SMART_ltc
from models.weighting.SMART_ltn import SMART_ltn
from models.weighting.SMART_lnu import SMART_lnu
from models.xml.XMLPreprocessor import XMLPreprocessor
from models.network.PageRank import PageRank
from utilities.utilities import load_queries_from_csv, create_or_load_collection, launch_run

DIR_SAVE='../../saves'
DIR_Q='../queries.csv'

class ARGS :
    def __init__(self) -> None:
        pass

# because pylint doesn't handle well polymorphism
# pylint: disable=redefined-variable-type
def main():
    args = ARGS()
    args.tokenizer = "nltk"
    args.lemmer = True
    args.parallel_computing = False
    args.generate_index = True
    args.pagerank = True
    args.anchors = False


    for granularity in [["article"]]: #(): # ["element"], , "title", "bdy", "p"
        XMLDocument.granularity = granularity

        for stopword in [True]: # False
            args.stopword = stopword

            for stemmer in ["porter"]: # "None",
                args.stemmer = stemmer

                collection = None # free memory
                collection = create_or_load_collection(args, "xml", False)

                if args.pagerank:
                    print("Computing pagerank...", file=stderr)
                    pr = PageRank(XMLPreprocessor.anchors).pagerank()
                else:
                    pr = None

                index_path = f"{DIR_SAVE}/index_regex_{stopword}_nltk_{stopword}_{stemmer}_collection5.pkl"
                print("Loading queries...", file=stderr)
                queries = load_queries_from_csv(DIR_Q)

                # for each weighting function
                ranking_function = SMART_ltn(N=len(collection))
                collection.information_retriever = ranking_function
                launch_run(collection, queries, index_path, "smart_ltn", [], pr)

                ranking_function = SMART_ltc(N=len(collection))
                collection.information_retriever = ranking_function
                launch_run(collection, queries, index_path, "smart_ltc", [], pr)

                for slope in (0.1, 0.2, 0.3, 0.4, 0.5):
                    ranking_function = SMART_lnu(N=len(collection), slope=slope)
                    collection.information_retriever = ranking_function
                    launch_run(collection, queries, index_path, "smart_lnu", [f"slope{slope}"], pr)

                for alpha_article in (0.5, 1):
                    for alpha_title in (2, 4, 5):
                        for alpha_bdy in (1.75, 2.86):
                            for alpha_p in (0.15, 5.67):

                                XMLDocument.granularity_weights = {
                                    "article" : alpha_article,
                                    "title" : alpha_title,
                                    "bdy" : alpha_bdy,
                                    "p" : alpha_p,
                                }
                                for k1 in [1.2]: # , 1.7, 2.2, 3.7
                                    for b in [0.75]: # 0.5, , 0.9
                                        tmp = {
                                            "bm25" : BM25,
                                            "bm25fw" : BM25Fw,
                                            "bm25fr" : BM25Fr
                                        }

                                        for name, ranking_function in tmp.items():
                                            collection.information_retriever = ranking_function(
                                                N=len(collection),
                                                avdl=collection.get_avdl(),
                                                b=b, k1=k1
                                                )
                                            launch_run(collection, queries, index_path, name, [f"k{k1}", f"b{b}"], pr)


if __name__ == "__main__":
    main()