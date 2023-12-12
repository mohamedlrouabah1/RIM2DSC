import os
from sys import stderr
from tqdm import tqdm

from models.xml.XMLCollection import XMLCollection
from models.IRrun import IRrun
from models.weighting.BM25 import BM25
from models.weighting.SMART_ltc import SMART_ltc
from models.weighting.SMART_ltn import SMART_ltn
from models.weighting.SMART_lnu import SMART_lnu
from utilities.utilities import load_queries_from_csv
from utilities.config import NB_RANKING

DIR_SAVE='../../saves'
DIR_Q='../queries.csv'

def main():
    save_dir = [f for f in os.listdir(DIR_SAVE) if f.lower().endswith('.pkl')]
    for pickle_file in tqdm(save_dir, desc="Iteraring saved collections ..."):
        file_path = os.path.join(DIR_SAVE, pickle_file)
        print(f"desealize {pickle_file}", file=stderr)
        collection = XMLCollection.deserialize(file_path)
        
        print("Loading queries...", file=stderr)
        queries = load_queries_from_csv(DIR_Q)

        # for each weighting function
        ranking_function = SMART_ltn(N=len(collection))
        collection.information_retriever = ranking_function
        rank(collection, queries, pickle_file, "smart_ltn", [])

        ranking_function = SMART_ltc(N=len(collection))
        collection.information_retriever = ranking_function
        rank(collection, queries, pickle_file, "smart_ltc", [])

        for slope in [0.1, 0.2, 0.3, 0.4, 0.5]:
            ranking_function = SMART_lnu(N=len(collection), slope=slope)
            collection.information_retriever = ranking_function
            rank(collection, queries, pickle_file, "smart_lnu", [f"slope{slope}"])

        
        for k1 in [1.2, 1.7, 2.2, 3.7]:
            for b in [0.5, 0.75, 0.9]:
                ranking_function = BM25(
                    N=len(collection),
                    avdl=collection.get_avdl(), 
                    b=b, k1=k1
                    )
                collection.information_retriever = ranking_function
                rank(collection, queries, pickle_file, "bm25", [f"k{k1}", f"b{b}"])




def rank(collection:XMLCollection, queries:list,file_name, a_ranking, a_params) -> None:
    # get infor from collection save file name
    tmp = file_name.split('_')
    a_stopword = tmp[2]
    a_stemmer = tmp[4]
    
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

        # we filter overlapping results
        nb_scores = 0
        run_lines = []
        run_lines.append(ranking[0])
        j = 1
        while nb_scores < NB_RANKING  and j < len(ranking):
            line_id, line_xpath = run_lines[nb_scores][0].split(':')
            doc_id, xpath = ranking[j][0].split(':')

            # does it overlap with the previous score ?
            if line_id == doc_id  and xpath.find(line_xpath) != -1:
                run_lines[nb_scores] = ranking[j]

            else:
                nb_scores += 1
                if nb_scores < NB_RANKING:
                    run_lines.append(ranking[j])

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
    main()