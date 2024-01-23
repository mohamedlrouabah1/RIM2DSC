from __future__ import annotations
from tqdm import tqdm

class PageRank():
    """
    Class for calculating PageRank scores for a given graph of links.

    Attributes:
        - default (float): Default value for PageRank damping factor, typically between 0 and 1. Defaults to 0.1.

    Methods:
        __init__(list_tag_link: list[tuple[str, str, list[str]]]): Initializes the PageRank object with a list of tag links.
        pagerank(d=0.85, max_iterations=100, convergence_threshold=1e-6) -> dict[str, float]:
            Calculates PageRank scores for the given graph.
    """

    default = 0.1

    def __init__(self, list_tag_link:list[tuple[str, str, list[str]]]):
        """
        create the graph of links from a list of tag links.
        Params:
        -------
        list_tag_link: (list[Tuple[str, str, list[str]]])
            list of tuples (doc_id, reffered_doc_id, anchor_tokens)
        """
        self.graph = {}
        for doc_id, referred_doc_id, _ in tqdm(list_tag_link, "Creating graph of links"):
            referred_doc_id = referred_doc_id.split(':')[0]
            if doc_id not in self.graph:
                self.graph[doc_id] = []
            self.graph[doc_id].append(referred_doc_id)

    def pagerank(self, d=0.85, max_iterations=5, convergence_threshold=1e-4) -> dict[str, float]:
        """
        Calculate PageRank scores for a given graph.

        Parameters:
        - graph (dict): A dictionary representing the graph of links. Keys are pages, and values are lists of pages
                        linked from the corresponding key page.
        - d (float, optional): Damping factor, typically between 0 and 1. It represents the probability that a user
                            will follow a link. Defaults to 0.85.
        - max_iterations (int, optional): Maximum number of iterations for the PageRank calculation. Defaults to 100.
e        - convergence_threshold (float, optional): Convergence threshold for stopping the iterations when the PageRank
                                                scores stabilize. Defaults to 1e-6.

        Returns:
        - dict: A dictionary containing PageRank scores for each page in the input graph.
        """
        # debug save the graph into a file
        with open("out_graph.txt", "w", encoding="utf-8") as f:
            for page, links in self.graph.items():
                f.write(f"{page}\t{links}\n")

        # Initialization of PageRank scores
        pr = {page: 1 / len(self.graph) for page in self.graph}

        for i in range(max_iterations):
            pr_new = {}
            for page in tqdm(self.graph, f"Computing PageRank scores, iteration {i}"):
                # Calculate the new PageRank score
                pr_new[page] = (1 - d) + d * sum(pr[link] / len(self.graph[link]) for link in self.graph if page in self.graph[link])

            # Check for convergence
            if all(abs(pr_new[page] - pr[page]) < convergence_threshold for page in self.graph):
                print(f"Converge at iteration {i}")
                if i > 4:
                    break

            # debug result
            with open(f"out_pagerank_iteration_{i}.txt", "w", encoding="utf-8") as f:
                for page, score in pr_new.items():
                    f.write(f"{page}\t{score}\n")

            pr = pr_new

        normalization_factor = 1 / sum(pr.values())
        pr = {page: score * normalization_factor for page, score in pr.items()}

        # debug save the page rank value into a file
        with open("pagerank.txt", "w", encoding="utf-8") as f:
            for page, score in pr.items():
                f.write(f"{page}\t{score}\n")

        return pr
