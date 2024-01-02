class PageRank():

    def pagerank(cls, graph, d=0.85, max_iterations=100, convergence_threshold=1e-6):
        """
        Calculate PageRank scores for a given graph.

        Parameters:
        - graph (dict): A dictionary representing the graph of links. Keys are pages, and values are lists of pages
                        linked from the corresponding key page.
        - d (float, optional): Damping factor, typically between 0 and 1. It represents the probability that a user
                            will follow a link. Defaults to 0.85.
        - max_iterations (int, optional): Maximum number of iterations for the PageRank calculation. Defaults to 100.
        - convergence_threshold (float, optional): Convergence threshold for stopping the iterations when the PageRank
                                                scores stabilize. Defaults to 1e-6.

        Returns:
        - dict: A dictionary containing PageRank scores for each page in the input graph.
        """

        # Initialization of PageRank scores
        pr = {page: 1 / len(graph) for page in graph}

        for _ in range(max_iterations):
            pr_new = {}
            for page in graph:
                # Calculate the new PageRank score
                pr_new[page] = (1 - d) + d * sum(pr[link] / len(graph[link]) for link in graph if page in graph[link])

            # Check for convergence
            if all(abs(pr_new[page] - pr[page]) < convergence_threshold for page in graph):
                break

            pr = pr_new

        normalization_factor = 1 / sum(pr.values())
        pr = {page: score * normalization_factor for page, score in pr.items()}

        return pr