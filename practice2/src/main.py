from utils import *
from generate_index import *
from plotting import *
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

    # Prompt the user for whether they want to print the index or not
    print_option = input("Do you want to print the index? (y/n): ").lower()
    should_print = print_option == "y"

    # Index the files and measure the time taken
    # times = index_files_and_measure_time(filenames, print_index=should_print)

    # Lists to store statistics for both methods
    stats_stemming_stopword = []
    stats_stopword_only = []
    stats_basic = []
    # To store time
    times_stemming_stopword = []
    times_stopword_only = []
    times_basic = []
    times_oop = []

    for file in filenames:
        doc = load_text_collection(f"{DATA_FOLDER}/{file}")

        # Timing and statistics for stemming + stopword method
        start_time = time_ns()
        stemming_stopword_index = generate_index_oop(doc, 1)
        end_time = time_ns()
        times_stemming_stopword.append(convert_time_from_ns_to_s(end_time - start_time))
        stats_stemming_stopword.append(get_index_statistics(stemming_stopword_index))

        # Timing and statistics for stopword only method
        start_time = time_ns()
        stopword_only_index = generate_index_oop(doc, 2)
        end_time = time_ns()
        times_stopword_only.append(convert_time_from_ns_to_s(end_time - start_time))
        stats_stopword_only.append(get_index_statistics(stopword_only_index))

        # Timing and statistics for basic method
        start_time = time_ns()
        basic_index= generate_index_oop(doc,3)
        end_time = time_ns()
        times_basic.append(convert_time_from_ns_to_s(end_time - start_time))
        stats_basic.append(get_index_statistics(basic_index))

        # Gather statistics for OOP method
        average_document_lengths_oop.append(sum(d.length for d in oop_index.collection.documents) / len(oop_index.collection.documents))
        average_term_lengths_oop.append(sum(len(term) for term in oop_index.get_vocabulary()) / oop_index.get_vocabulary_size())
        vocabulary_sizes_oop.append(oop_index.get_vocabulary_size())
        total_collection_frequencies_oop.append(sum(oop_index.get_term_frequency(term) for term in oop_index.get_vocabulary()))
    
    if not should_print:
        # Plotting
        plot_efficiency_and_statistics_graphs(file_sizes, times_stemming_stopword, stats_stemming_stopword, f"{RENDU_FOLDER}/efficiency_and_statistics_graph_stemming.png")
        plot_efficiency_and_statistics_graphs(file_sizes, times_stopword_only, stats_stopword_only, f"{RENDU_FOLDER}/efficiency_and_statistics_graph_stopwordonly.png")
        plot_efficiency_and_statistics_graphs(file_sizes, times_basic, stats_basic, f"{RENDU_FOLDER}/efficiency_and_statistics_graph_basic.png")
        # Print results directly to terminal and write to the file
        with open(f"{RENDU_FOLDER}/time_comparison.txt", 'w') as file:
            header = "\nSize of Collection (KB) | Time Stemmer Stop word | Time Stop word only | Time Basic"
            separator = "\n" + "-" * len(header)

            print(header)
            print(separator)
            file.write(header + separator)

            for size, t_basic, t_stemming, t_stopword in zip(file_sizes,times_basic, times_stemming_stopword, times_stopword_only):
                line = f"\n{size:>25} KB | {t_stemming:>12.2f} sec | {t_stopword:>12.2f} sec | {t_basic:>9.2f} sec"
                print(line)
                file.write(line)

            file.write("\n" + "-" * len(header))
            print("\n" + "-" * len(header))
    else:
        # Prompt the user for which version of the index to print
        print_option = input("Do you want to print the index Stemming/stop-word or basic? (s=stemming/t=stop-word/n=basic): ").lower()
        if print_option == "s":
            print("Creating... Inverted Index Time for Each File For Stemming version (in seconds)\nLoading...")
            with open(f"{RENDU_FOLDER}/IDF_Time_File_stemming.txt", 'w') as f:
                for file, time_duration in zip(filenames, times_stemming_stopword):
                    term_dicts = []

                    for term, posting_list in stemming_stopword_index.posting_lists.items():
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
            print("*******completed for Stemming version!*********")
        elif print_option == "t":
            print("Creating... Inverted Index Time for Each File For Stop-word version (in seconds)\nLoading...")
            with open(f"{RENDU_FOLDER}/IDF_Time_File_stopword.txt", 'w') as f:
                for file, time_duration in zip(filenames, times_stopword_only):
                    term_dicts = []

                    for term, posting_list in stopword_only_index.posting_lists.items():
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
            print("*******completed for Stop-word version!*********")
        elif print_option == "n":
            print("Creating... Inverted Index Time for Each File For Basic version (in seconds)\nLoading...")
            with open(f"{RENDU_FOLDER}/IDF_Time_File_basic.txt", 'w') as f:
                for file, time_duration in zip(filenames, times_basic):
                    term_dicts = []

                    for term, posting_list in basic_index.posting_lists.items():
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
            print("*******completed for Basic version!*********")

if __name__ == "__main__":
    main()
