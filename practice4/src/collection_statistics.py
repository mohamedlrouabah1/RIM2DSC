import os
from time import time_ns
import matplotlib.pyplot as plt
from generate_index import generate_index_oop, get_index_statistics
from utilities.config import GRAPH_FOLDER, DATA_FOLDER, COLLECTION_FILES   
from utilities.utils import load_text_collection
from utilities.time_utility import print_time, convert_time_from_ns_to_s


def collection_statistics(mode, chartname) :
    collection_sizes = []
    doc_lengths = []
    term_lengths = []
    vocab_sizes = []
    coll_frequencies = []
    indexing_times = []
    pre_processing_times = []
    file_path = COLLECTION_FILES[0]
        
    content = load_text_collection(f"{DATA_FOLDER}/{file_path}")
    
    index = generate_index_oop(content,mode)
    
    avg_doc_len, avg_term_len, vocab_size, total_coll_freq = get_index_statistics(index)

    # Collecting data for plotting
    collection_sizes.append(os.path.getsize(os.path.join(DATA_FOLDER, file_path)) / 1024)
    doc_lengths.append(avg_doc_len)
    term_lengths.append(avg_term_len)
    vocab_sizes.append(vocab_size)
    coll_frequencies.append(total_coll_freq)
    indexing_times.append(convert_time_from_ns_to_s(index.indexing_time_in_ns))
    pre_processing_times.append(convert_time_from_ns_to_s(index.preprocessing_time_in_ns))
    # Printing data
    print("----------------------------------------")
    print(f"Indexing file: {file_path}")
    print(f"Average Document Length: {avg_doc_len} (words)")
    print(f"Average Term Length: {avg_term_len} (characters)")
    print(f"Vocabulary Size: {vocab_size} (unique terms)")
    print(f"Total Collection Frequency: {total_coll_freq} (terms)")
    print("Indexation time: ")
    print_time(chartname,index.indexing_time_in_ns)
    print("Preprocessing time: ")
    print_time(chartname,index.preprocessing_time_in_ns)
    print("----------------------------------------")
        

   # Display metrics using an improved bar plot
    labels = ["Avg Doc Length", "Avg Term Length", "Vocabulary Size", "Total Collection Frequency", "Time (seconds)"]
    values = [doc_lengths[0], term_lengths[0], vocab_sizes[0], coll_frequencies[0], indexing_times[0]]

    plt.figure(figsize=(12, 8))
    bars = plt.bar(labels, values, color=['blue', 'green', 'red', 'purple', 'cyan'])
    
    # Use logarithmic scale for y-axis
    plt.yscale('log')
    plt.ylabel('Value (log scale)')
    plt.title(f'Metrics for the Collection: {COLLECTION_FILES[0]}')
    # Define units or descriptors
    units = ["(words)", "(characters)", "(unique terms)", "(terms)", "(seconds)"]

    # Annotate with exact values and units
    for i, bar in enumerate(bars):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + (0.02 * yval), f"{round(yval, 2)} {units[i]}", ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_FOLDER, f"{chartname}_Metrics_Bar_Plot.png"))
    plt.show()
    