from __future__ import annotations
import os

from models.concepts.InformationRessource import InformationRessource
from models.network.PageRank import PageRank
from models.xml.XMLDocument import XMLDocument

class IRrun:
    """
    Class for managing and saving Information Retrieval runs.

    Class Attributes:
    -----------------
    - NB_RANKING: int
        Number of top-ranked results to consider.
    - GROUP_NAME: str
        Group name for identifying the team in the run file.
    - ID_FILE_PATH: str
        File path for storing the last used run ID.
    - STOPLIST_SIZE: int
        Size of the stop-list.

    Methods:
    --------
    - __init__(self, weighting_function_name:str, stop:list[str], stem:str, params:dict) -> None:
        Constructor for IRrun.
    - ranking(self, collection, queries, pagerank:dict[str, float]=None):
        Rank documents based on queries and optionally incorporate PageRank scores.
    - save_run(self, verbose=False) -> bool:
        Save the run file to the specified file path.
    - load_last_id(self) -> int:
        Load the last used run ID from the file.
    - save_last_id(self, last_id):
        Save the last used run ID to the file.
    - _create_file_path(self, weighting_function, stop, stem, params):
        Create the file path for the run file.
    - _delOverlappingXMLElement(self, ranking:list[tuple[str, float]]) -> list[tuple[str, float]]:
        Remove overlapping rankings from a run result list.
    - _extractBestScores(self, ranking:list[tuple[str, float]]) -> list[tuple[str, float]]:
        Extract the best scores from a run result list.
    - _delIntertwinedResults(self, ranking:list[tuple[str, float]]) -> list[tuple[str, float]]:
        Remove intertwined results from a run result list.
    - _writeResultLine(self, query_id:str, doc_id:str, rank:int, score:float) -> None:
        Write a result line for an INEX run file.
    - _debugDisplayTopN(self, ranking:list[tuple[str, float]], top_n:int=10):
        Display the top N results of a ranking for debugging purposes.

    """
    NB_RANKING = 1500
    GROUP_NAME="MohammedWilliam"
    ID_FILE_PATH="../../last_id.txt"
    STOPLIST_SIZE = 671

    # for the display
    delimiter = "-" * 80
    top_n = 10

    def __init__(self, weighting_function_name:str, stop:list[str], stem:str, params:dict) -> None:
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

        if weighting_function_name in ("bm25fw", "bm25fr"):
            self.run_type = 'article'
        else:
            self.run_type = 'element'

    def ranking(self, collection:list[InformationRessource], queries:list[str], pagerank:dict[str, float]=None) :
        """
        Rank documents based on queries and optionally incorporate PageRank scores.

        Params:
        -------
        - collection: Collection
            The collection of documents.
        - queries: list
            List of queries.
        - pagerank: dict[str, float], optional
            PageRank scores for documents.
        """
        for query_id, query in queries:
            query_id = int(query_id)
            print(f"Query: {query}")
            collection.Timer.start(f"query{query_id:02d}_preprocessing")
            query = collection.preprocessor._text_preprocessing(query)
            collection.Timer.stop()
            print(f"Query preprocessed in {collection.Timer.get_time(f'query{query_id:02d}_preprocessing')}")
            print(f"Query preprocessed: {query}\n{self.delimiter}")

            print('Ranking documents...')
            collection.Timer.start(f"query{query_id:02d}_ranking")
            ranking = collection.compute_RSV(query)
            collection.Timer.stop()
            print(f"Documents ranked in {collection.Timer.get_time(f'query{query_id:02d}_ranking')}\n{self.delimiter}")
            print()

            if pagerank:
                print('Ponderate ranking with pagerank...')
                collection.Timer.start(f"query{query_id:02d}_pagerank")
                tmp = []
                PageRank.default = min(pagerank.values())
                for xpath, score in ranking:
                    doc_id = xpath.split(':')[0]
                    if doc_id in pagerank:
                        tmp.append((xpath, score * pagerank[doc_id]))
                    else:
                        tmp.append((xpath, score * PageRank.default))
                ranking = tmp
                collection.Timer.stop()
                print(f"Scores ponderated with pagerank in {collection.Timer.get_time(f'query{query_id:02d}_pagerank')}\n{self.delimiter}")
                print()

            if self.run_type == 'element':
                ranking = self._delOverlappingXMLElement(ranking)
                ranking = self._extractBestScores(ranking)
                ranking = self._delIntertwinedResults(ranking)

                for i, (doc_id, _) in enumerate(ranking):
                    rank = i+1
                    self._writeResultLine(query_id=query_id, doc_id=doc_id, rank=rank, score=self.NB_RANKING - rank)

            else: # 'article
                ranking = self._extractBestScores(ranking)

                for i, (doc_id, score) in enumerate(ranking):
                    rank = i+1
                    self._writeResultLine(query_id, doc_id, rank, score)


    def save_run(self, verbose=False) -> bool:
        """
        Save the run file to the specified file path.

        Params:
        -------
        - verbose: bool, optional
            Flag indicating whether to display verbose output.

        Returns:
        --------
        bool
            True if the save operation is successful, False otherwise.

        """
        try:
            if verbose: print(f"Saving run file to {self.file_path}...")

            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(self.run_as_str)

            if verbose: print('Done.')

            return True

        except IOError:
            print(f"Error while saving run file to {self.file_path}.")
            return False


    def load_last_id(self) -> int:
        """
        Load the last used run ID from the file.

        Returns:
        --------
        int
            Last used run ID.

        """
        if os.path.exists(IRrun.ID_FILE_PATH):
            with open(IRrun.ID_FILE_PATH, "r", encoding="utf-8") as file:
                last_id = int(file.read())
            return last_id

        return 0

    def save_last_id(self, last_id):
        """
        Save the last used run ID to the file.

        Params:
        -------
        - last_id
            Last used run ID.

        """
        with open(IRrun.ID_FILE_PATH, "w", encoding="utf-8") as file:
            file.write(str(last_id))


    def _create_file_path(self, weighting_function, stop, stem, params):
        """
        Create the file path for the run file.

        Params:
        -------
        - weighting_function
            Name of the weighting function.
        - stop: list[str]
            Stoplist configuration.
        - stem: str
            Stemming configuration.
        - params: dict
            Other interesting parameters used.

        Returns:
        --------
        str
            File path for the run file.

        """
        stop = f"stop{IRrun.STOPLIST_SIZE}" if stop else "nostop"
        stem = stem if stem else "nostem"
        params = '_'.join(params)
        if weighting_function in ("bm25fw", "bm25fr"):
            for tag, alpha in XMLDocument.granularity_weights.items():
                params += f"_alpha{tag}{alpha}"
        granularity = '_'.join(XMLDocument.granularity)

        return f"../results/{IRrun.GROUP_NAME}_{self.id}_{weighting_function}_{granularity}_{stop}_{stem}_{params}.txt"


    def _delOverlappingXMLElement(self, ranking:list[tuple[str, float]]) -> list[tuple[str, float]]:
        """
        Remove overlapping rankings from a run result list.

        Params:
        -------
        - ranking: list[tuple[str, float]]
            List of tuple (doc_id, score) sorted by doc_id.

        Returns:
        --------
        list[tuple[str, float]]
            List of tuple (doc_id, score) without overlapping scores.

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


    def _extractBestScores(self, ranking:list[tuple[str, float]]) -> list[tuple[str, float]]:
        """
        Extract the best scores from a run result list.

        Params:
        -------
        - ranking: list[tuple[str, float]]
            List of tuple (doc_id, score) sorted by score.

        Returns:
        --------
        list[tuple[str, float]]
            List of tuple (doc_id, score) with the best scores.

        """
        ranking.sort(key=lambda x: x[1], reverse=True)
        return ranking[:IRrun.NB_RANKING]


    def _delIntertwinedResults(self, ranking:list[tuple[str, float]]) -> list[tuple[str, float]]:
        """
        Remove intertwined results from a run result list.

        Params:
        -------
        - ranking: list[tuple[str, float]]
            List of tuple (doc_id, score) sorted by doc_id.

        Returns:
        --------
        list[tuple[str, float]]
            List of tuple (doc_id, score) without intertwined results.

        """
        ranking.sort(key=lambda x: x[0])
        return ranking

    def _writeResultLine(self, query_id:str, doc_id:str, rank:int, score:float) -> None:
        """
        Create a result line for an INEX run file.
        Note: the scores are modified in order to be decreasing with the rank.

        Params:
        -------
        - query_id: str
            Query ID.
        - doc_id: str
            Document ID.
        - rank: int
            Rank of the document.
        - score: float
            Score of the document.
        """
        if ":" in doc_id:
            doc_id, xpath = doc_id.split(':')
            xpath.replace('/', '_')

        result_line = f"{query_id} Q0 {doc_id.split(':')[0]} {rank} {score} {IRrun.GROUP_NAME}{self.id} {xpath}\n"
        self.run_as_str += result_line

    def _debugDisplayTopN(self, ranking:list[tuple[str, float]], top_n:int=10):
        """
        Display the top N results of a ranking for debugging purposes.
        """
        print("Ranking results:")
        for i, (doc_id, score) in enumerate(ranking[:top_n]):
            print(f"#{i+1} - Document {doc_id} with score {score}")
        print(self.delimiter)
        print("\n\n")
