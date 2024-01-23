from sys import stderr

from models.xml.XMLDocument import XMLDocument
from models.weighting.BM25 import BM25
from models.weighting.BM25L import BM25L
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
    args.stopword = True
    args.stemmer = "porter"

    for tmp in [(True, False), (False, False), (False, True), (True, True)]:
        args.pagerank, args.anchors = tmp
        params = []
        if args.pagerank:
            params.append("pagerank")
        if args.anchors:
            params.append("anchors")

        for granularity in [["title", "bdy", "p"]]:
            XMLDocument.granularity = granularity


            collection = None # free memory
            collection = create_or_load_collection(args, "xml", False)

            if args.pagerank:
                print("Computing pagerank...", file=stderr)
                pr = PageRank(XMLPreprocessor.anchors).pagerank()
            else:
                pr = None

            index_path = f"{DIR_SAVE}/index_regex_{args.stopword}_nltk_{args.stopword}_{args.stemmer}_collection5.pkl"
            print("Loading queries...", file=stderr)
            queries = load_queries_from_csv(DIR_Q)

            # for each weighting function
            ranking_function = SMART_ltn(N=len(collection))
            collection.information_retriever = ranking_function
            launch_run(collection, queries, index_path, "smart_ltn", params, pr)

            ranking_function = SMART_ltc(N=len(collection))
            collection.information_retriever = ranking_function
            launch_run(collection, queries, index_path, "smart_ltc", params, pr)

            for slope in [0.1, 0.5]:
                ranking_function = SMART_lnu(N=len(collection), slope=slope)
                collection.information_retriever = ranking_function
                launch_run(collection, queries, index_path, "smart_lnu", params + [f"slope{slope}"], pr)

            k1, b = 1.2, 0.75
            for alpha_article in [0.5, 1]:
                for alpha_title in [2, 5]:
                    for alpha_bdy in [1.75, 2.86]:
                        for alpha_p in [2.15, 5]:

                            XMLDocument.granularity_weights = {
                                "article" : alpha_article,
                                "title" : alpha_title,
                                "bdy" : alpha_bdy,
                                "p" : alpha_p,
                            }

                            tmp = {
                                "bm25fw" : BM25Fw,
                                "bm25fr" : BM25Fr
                            }

                            for name, ranking_function in tmp.items():
                                collection.information_retriever = ranking_function(
                                    N=len(collection),
                                    avdl=collection.get_avdl(),
                                    b=b, k1=k1
                                    )
                                launch_run(collection, queries, index_path, name, params + [f"k{k1}", f"b{b}"], pr)

            for k3 in [0.5, 1.15, 2.34, 3.2, 6]:
                ranking_function = BM25L(
                    N=len(collection),
                    avdl=collection.get_avdl(),
                    b=b, k1=k1, k3=k3
                )
                collection.information_retriever = ranking_function
                launch_run(collection, queries, index_path, "bm25l", params + [f"k{k1}", f"b{b}", f"k3{k3}"], pr)


            for k1 in [1.2 , 1.7, 2.2, 3.7]:
                 for b in [0.25, 0.75]:
                    collection.information_retriever = BM25(
                        N=len(collection),
                        avdl=collection.get_avdl(),
                        b=b, k1=k1
                    )
                    launch_run(collection, queries, index_path, name, params + [f"k{k1}", f"b{b}"], pr)



if __name__ == "__main__":
    main()