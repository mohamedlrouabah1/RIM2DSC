from utils import load_text_collection, index_files_and_measure_time, DATA_FOLDER, RENDU_FOLDER
from generate_index import generate_index, generate_index_oop
from plotting import plot_efficiency_graph, plot_statistics_evolution, initialize_combined_plot, finalize_combined_plot
from time import time_ns
from utilities.time_utility import convert_time_from_ns_to_s, print_time
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')
def main() -> None:
    """
    Main function of the program. It will index the files and measure the time taken to do so.
    It will then plot the efficiency graph and statistics evolution graph.

    :return: None
    """
    filenames = [
        '01-Text_Only-Ascii-Coll-1-10-NoSem.gz',
        '02-Text_Only-Ascii-Coll-11-20-NoSem.gz',
        '03-Text_Only-Ascii-Coll-21-50-NoSem.gz',
        '04-Text_Only-Ascii-Coll-51-100-NoSem.gz',
        '05-Text_Only-Ascii-Coll-101-200-NoSem.gz',
        '06-Text_Only-Ascii-Coll-201-500-NoSem.gz',
        '07-Text_Only-Ascii-Coll-501-1000-NoSem.gz',
        '08-Text_Only-Ascii-Coll-1001-2000-NoSem.gz',
        '09-Text_Only-Ascii-Coll-2001-5000-NoSem.gz'
    ]
    file_sizes = [55, 52, 103, 96, 357, 559, 747, 1200, 4200]  # in KB
     # Provide an option to print the index or not
    print_option = input("Do you want to print the index? (y/n): ").lower()
    should_print = print_option == "y"
    # Index the files and measure the time taken
    times = index_files_and_measure_time(filenames, print_index=should_print)
    
    # Lists to store statistics for both methods
    average_document_lengths_basic = []
    average_term_lengths_basic = []
    vocabulary_sizes_basic = []
    total_collection_frequencies_basic = []

    average_document_lengths_oop = []
    average_term_lengths_oop = []
    vocabulary_sizes_oop = []
    total_collection_frequencies_oop = []

    # To store time
    times_basic = []
    times_oop = []

    for file in filenames:
        doc = load_text_collection(f"{DATA_FOLDER}/{file}")
         # Timing for basic method
        start_time = time_ns()
        basic_index, _, _ = generate_index(doc)
        end_time = time_ns()
        times_basic.append(convert_time_from_ns_to_s(end_time - start_time))

        # Gather statistics for basic method
        average_document_lengths_basic.append(sum(len(doc_id) for doc_id in basic_index) / len(basic_index))
        average_term_lengths_basic.append(sum(len(term) for term in basic_index) / len(basic_index))
        vocabulary_sizes_basic.append(len(basic_index))
        total_collection_frequencies_basic.append(sum(len(docs) for docs in basic_index.values()))

        # Timing for OOP method
        start_time = time_ns()
        oop_index = generate_index_oop(doc)
        end_time = time_ns()
        times_oop.append(convert_time_from_ns_to_s(end_time - start_time))

        # Gather statistics for OOP method
        average_document_lengths_oop.append(sum(d.length for d in oop_index.collection.documents) / len(oop_index.collection.documents))
        average_term_lengths_oop.append(sum(len(term) for term in oop_index.get_vocabulary()) / oop_index.get_vocabulary_size())
        vocabulary_sizes_oop.append(oop_index.get_vocabulary_size())
        total_collection_frequencies_oop.append(sum(oop_index.get_term_frequency(term) for term in oop_index.get_vocabulary()))
    
    if not should_print:
        # Plotting
        initialize_combined_plot()
        plot_efficiency_graph(file_sizes, times_basic)
        plot_statistics_evolution(file_sizes, average_document_lengths_basic, average_term_lengths_basic, vocabulary_sizes_basic, total_collection_frequencies_basic)
        finalize_combined_plot(f"{RENDU_FOLDER}/efficiency_and_statistics_graph_basic.png")

        initialize_combined_plot()
        plot_efficiency_graph(file_sizes, times_oop)
        plot_statistics_evolution(file_sizes, average_document_lengths_oop, average_term_lengths_oop, vocabulary_sizes_oop, total_collection_frequencies_oop)
        finalize_combined_plot(f"{RENDU_FOLDER}/efficiency_and_statistics_graph_oop.png")
        
        # Print results directly to terminal and write to the file
        with open(f"{RENDU_FOLDER}/time_comparison.txt", 'w') as file:
            header = "\nSize of Collection (KB) | Time (seconds) | Time OOP (seconds)"
            separator = "\n" + "-" * len(header)

            print(header)
            print(separator)
            file.write(header + separator)

            for size, t_basic, t_oop in zip(file_sizes, times_basic, times_oop):
                line = f"\n{size:>25} KB | {t_basic:>12.2f} sec | {t_oop:>12.2f} sec"
                print(line)
                file.write(line)

            file.write("\n" + "-" * len(header))
            print("\n" + "-" * len(header))

    if should_print:
        # Provide an option to print the index or not
        print_option = input("Do you want to print the index Stemming/stop-word or basic? (y=stemming/n=basic): ").lower()
        steeming_print = print_option == "y"
        if steeming_print:
            print("Creating... Inverted Index Time for Each File For basic version (in seconds)\nLoading...")
            with open(f"{RENDU_FOLDER}/IDF_Time_File_basic.txt", 'w') as f:  # Open the file for writing
                for file, time_duration in zip(filenames, times_basic):
                    # doc = load_text_collection(f"{DATA_FOLDER}/{file}")
                    # basic_index, _, _ = generate_index(doc)

                    term_dicts = []

                    for term, postings in basic_index.items():
                        term_dict = {}
                        term_dict["Term"] = term
                        term_dict["DF"] = len(postings)
                        term_dict["Postings List"] = ', '.join(f"{posting[0]} {posting[1]}" for posting in postings)
                        term_dicts.append(term_dict)

                    f.write(f"\nIndex for {file} (Indexed in {time_duration:.2f} seconds):\n")
                    f.write("---------------------------------------\n")
                    f.write("Term | DF | Postings List\n")
                    for td in term_dicts:
                        f.write(f"{td['Term']} | {td['DF']} | {td['Postings List']}\n")
                    f.write("\n---------------------------------------\n")
                    f.write("Term | DF | Postings List\n")
            print("*******completed for basic version!*********")

        # version without stemming using orient object programming 
        if not steeming_print :
            print("Creating... Inverted Index Time for Each File For OOP version (in seconds)\nLoading...")
            with open(f"{RENDU_FOLDER}/IDF_Time_File_OOP.txt", 'w') as f:  # Open the file for writingù
                
                for file, time_duration in zip(filenames, times):
                    # doc = load_text_collection(f"{DATA_FOLDER}/{file}")
                    # index = generate_index_oop(doc)

                    term_dicts = []

                    for term, posting_list in oop_index.posting_lists.items():
                        term_dict = {}
                        term_dict["Term"] = term
                        term_dict["DF"] = posting_list.document_frequency
                        term_dict["Postings List"] = ', '.join(f"{plu.document_id} {plu.frequency}" for plu in posting_list.postings.values())
                        term_dicts.append(term_dict)

                    f.write(f"\nIndex for {file} (Indexed in {time_duration:.2f} seconds):\n")
                    f.write("---------------------------------------\n")
                    f.write("Term | DF | Postings List\n")
                    for td in term_dicts:
                        f.write(f"{td['Term']} | {td['DF']} | {td['Postings List']}\n")
                    f.write("\n---------------------------------------\n")
                    f.write("Term | DF | Postings List\n")

            print("*******completed !*********")

   

if __name__ == "__main__":
    main()
