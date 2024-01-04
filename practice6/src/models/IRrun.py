import os
from typing import List, Tuple

from models.xml.XMLDocument import XMLDocument

class IRrun:
    NB_RANKING = 1500
    GROUP_NAME="MohammedWilliam"
    ID_FILE_PATH="../../last_id.txt"
    STOPLIST_SIZE = 671

    # for the display
    delimiter = "-" * 80
    top_n = 10

    def __init__(self, weighting_function_name:str, stop:List[str], stem:str, params:dict) -> None:
        """
        the filename of your runs should be named using the following template:
        TeamName_Run-Id_WeigthingFunction_Granularity_Stop_Stem_Parameters.txt
        With:
        - Run-Id = unique identifier
        - WeightingFunction = ltn, ltc, bm25, etc.
        - Stop ϵ { nostop, stopN } with N = size of the stop-list.
        - Stem ϵ { nostem, porter, lovins, paice, etc. }
        - Parameters: list all the other interesting parameters used, together with their value.
        Example: VictorAlbertJulesIsaac_12_bm25_elements_sec_p_stop344_nostem_k1.2_b0.75.txt
        """
        self.id = self.load_last_id()
        self.id += 1
        self.save_last_id(self.id)
        self.id = f"{self.id:02d}"

        self.file_path = self._create_file_path(weighting_function_name, stop, stem, params)
        self.run_as_str = ""

        if weighting_function_name == "bm25fw" or weighting_function_name == "bm25fr":
            self.run_type = 'article'
        else:
            self.run_type = 'element'

    def ranking(self, collection, queries) :
        for id, query in queries:
            id = int(id)
            print(f"Query: {query}")
            collection.Timer.start(f"query{id:02d}_preprocessing")
            query = collection.preprocessor._text_preprocessing(query)
            collection.Timer.stop()
            print(f"Query preprocessed in {collection.Timer.get_time(f'query{id:02d}_preprocessing')}")
            print(f"Query preprocessed: {query}\n{self.delimiter}")

            print(f"Ranking documents...")
            collection.Timer.start(f"query{id:02d}_ranking")
            ranking = collection.compute_RSV(query)
            collection.Timer.stop()
            print(f"Documents ranked in {collection.Timer.get_time(f'query{id:02d}_ranking')}\n{self.delimiter}")
            print()

            if self.run_type == 'element':
                ranking = self._delOverlappingXMLElement(ranking)
                ranking = self._extractBestScores(ranking)
                ranking = self._delIntertwinedResults(ranking)

                for i, (doc_id, _) in enumerate(ranking):
                    rank = i+1
                    self._writeResultLine(query_id=id, doc_id=doc_id, rank=rank, score=self.NB_RANKING - rank)

            else: # 'article
                ranking = self._extractBestScores(ranking)

                for i, (doc_id, score) in enumerate(ranking):
                    rank = i+1
                    self._writeResultLine(query_id=id, doc_id=doc_id, rank=rank, score=score)


    def save_run(self, verbose=False) -> bool:
        try:
            if verbose: print(f"Saving run file to {self.file_path}...")

            with open(self.file_path, "w") as f:
                f.write(self.run_as_str)

            if verbose: print("Done.")

            return True

        except IOError:
            print(f"Error while saving run file to {self.file_path}.")
            return False


    def load_last_id(self) -> int:
        if os.path.exists(IRrun.ID_FILE_PATH):
            with open(IRrun.ID_FILE_PATH, "r") as file:
                last_id = int(file.read())
            return last_id
        else:
            return 0

    def save_last_id(self, last_id):
        with open(IRrun.ID_FILE_PATH, "w") as file:
            file.write(str(last_id))


    def _create_file_path(self, weighting_function, stop, stem, params):
        """
        Internal used to create the file path of the run file at the initialization of the object.
        """
        stop = f"stop{IRrun.STOPLIST_SIZE}" if stop else "nostop"
        stem = stem if stem else "nostem"
        params = '_'.join(params)
        if weighting_function in ["bm25fw", "bm25fr"]:
            for tag, alpha in XMLDocument.granularity_weights.items():
                params += f"_alpha{tag}{alpha}"
        granularity = '_'.join(XMLDocument.granularity)

        return f"../results/{IRrun.GROUP_NAME}_{self.id}_{weighting_function}_{granularity}_{stop}_{stem}_{params}.txt"

    def _delOverlappingXMLElement(self, ranking:List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        """
        Remove overlapping rankings from a run result list.

        Params:
            ranking: list of tuple (doc_id, score) sorted by doc_id

        Return:
            list of tuple (doc_id, score) without overlapping scores
        """
        nb_scores, j, n = 0, 1, len(ranking)
        run_lines = [ranking[0]]

        while nb_scores < n  and j < n:
            line_id, line_xpath = run_lines[nb_scores][0].split(':')
            doc_id, xpath = ranking[j][0].split(':')

            # does it overlap with the previous score ?
            if line_id == doc_id  and xpath.find(line_xpath) != -1:
                run_lines[nb_scores] = ranking[j]
            else:
                run_lines.append(ranking[j])
                nb_scores += 1

            j+=1

        return run_lines


    def _extractBestScores(self, ranking:List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        """
        Extract the best scores from a run result list.

        Params:
            ranking: list of tuple (doc_id, score) sorted by score

        Return:
            list of tuple (doc_id, score) with the best scores
        """
        ranking.sort(key=lambda x: x[1], reverse=True)
        return ranking[:IRrun.NB_RANKING]


    def _delIntertwinedResults(self, ranking:List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        """
        Remove intertwined results from a run result list.

        Params:
            ranking: list of tuple (doc_id, score) sorted by doc_id

        Return:
            list of tuple (doc_id, score) without intertwined results
        """
        ranking.sort(key=lambda x: x[0])
        return ranking

    def _writeResultLine(self, query_id:str, doc_id:str, rank:int, score:float) -> None:
        """
        Create a result line for a INEX run file.
        Note: the scores are modified in order to be decresing with the rank.
        """
        if ":" in doc_id:
            doc_id, xpath = doc_id.split(':')
            xpath.replace('/', '_')

        result_line = f"{query_id} Q0 {doc_id.split(':')[0]} {rank} {score} {IRrun.GROUP_NAME}{self.id} {xpath}\n"
        self.run_as_str += result_line

    def _debugDisplayTopN(self, ranking:list[tuple[str, float]], top_n:int=10):
        print(f"Ranking results:")
        for i, (doc_id, score) in enumerate(ranking[:top_n]):
            print(f"#{i+1} - Document {doc_id} with score {score}")
        print(self.delimiter)
        print("\n\n")
