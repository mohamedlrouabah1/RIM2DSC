from utils import read_doc, generate_grid, index_files_and_measure_time
import matplotlib.pyplot as plt

def main() -> None:
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
    print_option = input("Do you want to print the index? (yes/no): ").lower()
    should_print = print_option == "yes"
    
    times = index_files_and_measure_time(filenames, print_index=should_print)

    # Plot the efficiency graph
    plt.plot(file_sizes, times, marker='o', linestyle='-')
    plt.xlabel('Size of Collection (KB)')
    plt.ylabel('Time (seconds)')
    plt.title('Time Efficiency of Indexing Program')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
