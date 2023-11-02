
class IRrun:
    GROUP_NAME="MohammedWilliam"

    def __init__(self) -> None:
        pass

    def create_result_line(self, query_id, doc_id, rank, score, run_id, xml_path):
        return f"{query_id} Q0 {doc_id} {rank} {score} {IRrun.GROUP_NAME}{run_id} {xml_path}\n"
    
    def create_file_path(self, run_id, weighting_function, granularity, stop, stem, params):
        """
        the filename of your runs should be named using the following template:
        TeamName_Run-Id_WeigthingFunction_Granularity_Stop_Stem_Parameters.txt
        With:
        - Run-Id = unique identifier
        - WeightingFunction = ltn, ltc, bm25, etc.
        - Granularity ϵ { articles, elements, passages }, i.e. the document unit. If “elements”, you can add the list
        of XML tags ϵ { article, header, title, bdy, sec, p, etc.} you consider as document units.
        - Stop ϵ { nostop, stopN } with N = size of the stop-list.
        - Stem ϵ { nostem, porter, lovins, paice, etc. }
        - Parameters: list all the other interesting parameters used, together with their value.
        Example: VictorAlbertJulesIsaac_12_bm25_elements_sec_p_stop344_nostem_k1.2_b0.75.txt
        """
        return f"../results/{IRrun.GROUP_NAME}_{run_id}_{weighting_function}_{granularity}_{stop}_{stem}_{'_'.join(params)}.txt"
    