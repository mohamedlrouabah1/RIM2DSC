import os
from time import time_ns
import matplotlib.pyplot as plt
from generate_index import *
from utils import *
from utilities.time_utility import *
def exercise2():
    collection_sizes = []
    doc_lengths = []
    term_lengths = []
    vocab_sizes = []
    coll_frequencies = []
    indexing_times = []

    for file_path in COLLECTION_FILES:
        
        content = load_text_collection(f"{DATA_FOLDER}/{file_path}")
 
        
        start_time_ns = time_ns()
        index = generate_index_oop(content)
        indexing_time = time_ns() - start_time_ns
        
        avg_doc_len, avg_term_len, vocab_size, total_coll_freq = get_index_statistics(index)

        # Collecting data for plotting
        collection_sizes.append(os.path.getsize(os.path.join(DATA_FOLDER, file_path)) / 1024)
        doc_lengths.append(avg_doc_len)
        term_lengths.append(avg_term_len)
        vocab_sizes.append(vocab_size)
        coll_frequencies.append(total_coll_freq)
        indexing_times.append(convert_time_from_ns_to_s(indexing_time))

        # Printing data
        print(f"Indexing file: {file_path}")
        print(f"Average Document Length: {avg_doc_len}")
        print(f"Average Term Length: {avg_term_len}")
        print(f"Vocabulary Size: {vocab_size}")
        print(f"Total Collection Frequency: {total_coll_freq}")
        print_time(indexing_time)
        print("----------------------------------------")

    # Plotting
    plt.figure(figsize=(10,6))
    
    plt.subplot(2, 2, 1)
    plt.plot(collection_sizes, doc_lengths, marker='o')
    plt.title("Average Document Length vs. Collection Size")
    plt.xlabel("Collection Size (KB)")
    plt.ylabel("Avg Document Length")
    
    plt.subplot(2, 2, 2)
    plt.plot(collection_sizes, term_lengths, marker='o')
    plt.title("Average Term Length vs. Collection Size")
    plt.xlabel("Collection Size (KB)")
    plt.ylabel("Avg Term Length")
    
    plt.subplot(2, 2, 3)
    plt.plot(collection_sizes, vocab_sizes, marker='o')
    plt.title("Vocabulary Size vs. Collection Size")
    plt.xlabel("Collection Size (KB)")
    plt.ylabel("Vocabulary Size")
    
    plt.subplot(2, 2, 4)
    plt.plot(collection_sizes, coll_frequencies, marker='o')
    plt.title("Total Collection Frequency vs. Collection Size")
    plt.xlabel("Collection Size (KB)")
    plt.ylabel("Total Collection Frequency")
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    exercise2()
