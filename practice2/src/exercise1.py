import time
from generate_index import generate_index_oop
from utils import *
from utilities.time_utility import *
import matplotlib.pyplot as plt
import os
def exercise1() :

    file_sizes_kb = []
    indexing_times_s = []

    for file_path in COLLECTION_FILES:
        print(f"Indexing {file_path}...")
        
        file_size_kb = os.path.getsize(os.path.join(DATA_FOLDER, file_path)) / 1024


        content = load_text_collection(f"{DATA_FOLDER}/{file_path}")
        
        start_time_ns = time.time_ns()
        index = generate_index_oop(content)
        end_time_ns = time.time_ns()

        indexing_time_ns = end_time_ns - start_time_ns
        indexing_time_s = convert_time_from_ns_to_s(indexing_time_ns)

        print_time(indexing_time_ns)
        
        file_sizes_kb.append(file_size_kb)
        indexing_times_s.append(indexing_time_s)

    plt.plot(file_sizes_kb, indexing_times_s, '-o')
    plt.xlabel('Size of Collection (KB)')
    plt.ylabel('Indexing Time (seconds)')
    plt.title('Time Efficiency of Indexing')
    plt.grid(True)
    plt.show()