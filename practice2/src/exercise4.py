from utils import *
from generate_index import *
from time import time_ns
from utilities.time_utility import *

def exercise4():
    
    start_time_ns = time_ns()
    index = generate_index_oop(load_text_collection(f"{DATA_FOLDER}/{COLLECTION_FILES[-1]}"))
    indexing_time = time_ns() - start_time_ns

    avg_doc_len, avg_term_len, vocab_size, total_coll_freq = get_index_statistics(index)
    
    print("Statistics after removing stopwords:")
    print(f"Average Document Length: {avg_doc_len}")
    print(f"Average Term Length: {avg_term_len}")
    print(f"Vocabulary Size: {vocab_size}")
    print(f"Total Collection Frequency: {total_coll_freq}")
    print_time(indexing_time)

if __name__ == "__main__":
    exercise4()
