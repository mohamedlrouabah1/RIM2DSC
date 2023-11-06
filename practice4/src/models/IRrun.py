import os

class IRrun:
    GROUP_NAME="MohammedWilliam"
    ID_FILE_PATH="../../last_id.txt"
    DEFAULT_GRANULARITY="/article[1]"
    STOPLIST_SIZE = 211 # nltk : 179, punctuations : 32, both : 211

    def __init__(self, weighting_function,stop, stem, params, granularity=None) -> None:
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
        self.id = self.load_last_id()
        self.id += 1
        self.save_last_id(self.id)
        self.id = f"{self.id:02d}"

        self.file_path = self.create_file_path(weighting_function, granularity, stop, stem, params)
        self.run_as_str = ""
    
    def create_file_path(self, weighting_function, granularity, stop, stem, params):
        """Internal used to create the file path of the run file at the initialization of the object."""
        granularity = IRrun.DEFAULT_GRANULARITY if not granularity else granularity
        granularity = granularity.replace("/", "")
        stop = f"stop{IRrun.STOPLIST_SIZE}" if stop else "nostop"
        stem = stem if stem else "nostem"
        return f"../results/{IRrun.GROUP_NAME}_{self.id}_{weighting_function}_{IRrun.DEFAULT_GRANULARITY if not granularity else granularity}_{stop}_{stem}_{'_'.join(params)}.txt"
    

    def add_result_line(self, query_id, doc_id, rank, score, xml_path="/article[1]"):
        result_line = f"{query_id} Q0 {doc_id} {rank} {score} {IRrun.GROUP_NAME}{self.id} {xml_path}\n"
        self.run_as_str += result_line
        return result_line
    

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