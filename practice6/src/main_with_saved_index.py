import os
from sys import stderr
from tqdm import tqdm

from models.xml.XMLCollection import XMLCollection
from models.weighting.BM25 import BM25
from models.weighting.SMART_ltc import SMART_ltc
from models.weighting.SMART_ltn import SMART_ltn
from models.weighting.SMART_lnu import SMART_lnu
from utilities.utilities import load_queries_from_csv, launch_run

DIR_SAVE='../../saves'
DIR_Q='../queries.csv'

def main():
    save_dir = [f for f in os.listdir(DIR_SAVE) if f.lower().endswith('.pkl')]
    for pickle_file in tqdm(save_dir, desc="Iteraring saved collections ..."):
        file_path = os.path.join(DIR_SAVE, pickle_file)
        print(f"desearialize {pickle_file}", file=stderr)
        collection = XMLCollection.deserialize(file_path)

        print("Loading queries...", file=stderr)
        queries = load_queries_from_csv(DIR_Q)

        # for each weighting function
        collection.information_retriever = SMART_ltn(N=len(collection))
        launch_run(collection, queries, pickle_file, "smart_ltn", [])

        collection.information_retriever = SMART_ltc(N=len(collection))
        launch_run(collection, queries, pickle_file, "smart_ltc", [])

        for slope in (0.1, 0.2, 0.3, 0.4, 0.5):
            collection.information_retriever = SMART_lnu(N=len(collection), slope=slope)
            launch_run(collection, queries, pickle_file, "smart_lnu", [f"slope{slope}"])


        for k1 in (1.2, 1.7, 2.2, 3.7):
            for b in (0.5, 0.75, 0.9):
                collection.information_retriever = BM25(
                    N=len(collection),
                    avdl=collection.get_avdl(),
                    b=b, k1=k1
                    )

                launch_run(collection, queries, pickle_file, "bm25", [f"k{k1}", f"b{b}"])




if __name__ == "__main__":
    main()