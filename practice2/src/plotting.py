import matplotlib.pyplot as plt

def initialize_combined_plot():
    """ Initialize a combined figure for plotting. """
    plt.figure(figsize=(15, 5))
    
def plot_efficiency_graph(file_sizes, times):
    plt.subplot(1, 2, 1)
    plt.plot(file_sizes, times, marker='o', linestyle='-')
    plt.xlabel('Size of Collection (KB)')
    plt.ylabel('Time (seconds)')
    plt.title('Time Efficiency of Indexing Program')
    plt.grid(True)
    plt.tight_layout()

def plot_statistics_evolution(file_sizes, avg_doc_lengths, avg_term_lengths, vocab_sizes, total_coll_freqs):
    plt.subplot(1, 2, 2)
    plt.plot(file_sizes, avg_doc_lengths, marker='o', linestyle='-', label="Avg. Doc Length")
    plt.plot(file_sizes, avg_term_lengths, marker='s', linestyle='--', label="Avg. Term Length")
    plt.plot(file_sizes, vocab_sizes, marker='d', linestyle='-.', label="Vocabulary Size")
    plt.plot(file_sizes, total_coll_freqs, marker='x', linestyle=':', label="Total Term Frequency")
    plt.xlabel('Size of Collection (KB)')
    plt.title('Statistics Evolution')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

def finalize_combined_plot(filename="what_ever.png"):
    """ 
    Save the combined plot as a PNG and then display it.
    
    Parameters:
    -----------
    filename : str, optional
        The name of the file where the plot will be saved. 
        By default, it's set to "combined_plot.png".
    """
    plt.savefig(filename, format="png", dpi=300)
    plt.show()
