"""
In this code we run the IncrementalPersonalizedPageRank2 class on a randomly generated graph to compute the
personalized page rank values. We simultaneously the page rank method given in the networkx library and compare
their values for different parameters.
"""
from __future__ import division
import networkx as nx
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from Page_Rank2 import IncrementalPersonalizedPageRank2
from Page_Rank import IncrementalPersonalizedPageRank
import numpy as np

random.seed(1)
graph = nx.DiGraph()
number_of_nodes = random.randint(2, 100)
nodes = range(number_of_nodes)
graph.add_nodes_from(nodes)
number_of_random_walks = 10
random_walk_length = 5
difference = list()

for _ in range(2 * number_of_nodes):
    node_1 = random.choice(list(graph.nodes()))
    node_2 = random.choice(list(set(graph.nodes()) - {node_1}))
    if graph.has_edge(node_1, node_2) or graph.has_edge(node_2, node_1):
        continue
    else:
        weight = random.randint(1, 10)
        graph.add_weighted_edges_from([(node_1, node_2, weight)])
nx.draw_circular(graph, node_size=30, with_labels=True)
plt.show()

while number_of_random_walks <= 600:
    number_of_random_walks += 200
    random_walk_length = 5
    while random_walk_length <= 100:
        random_walk_length += 1
        pr = IncrementalPersonalizedPageRank(graph, 0, number_of_random_walks, 0.05, random_walk_length)
        pr.initial_random_walks()
        page_ranks = pr.compute_personalized_page_ranks()
        page_ranks_2 = nx.pagerank(pr.graph, alpha=0.95, personalization={0: 1},
                                   max_iter=500, weight='weight')

        difference.append(np.linalg.norm(np.array(page_ranks.values()) - np.array(page_ranks_2.values())) /
                          np.linalg.norm(page_ranks_2.values()))

plt.plot(range(6, 101), difference[0:95], 'r', range(6, 101), difference[96:191], 'g',
         range(6, 101), difference[192:287], 'y')
red_patch = mpatches.Patch(color='red', label='210 Random Walks')
green_patch = mpatches.Patch(color='green', label='410 Random Walks')
yellow_patch = mpatches.Patch(color='yellow', label='610 Random Walks')
plt.legend(handles=[red_patch, green_patch, yellow_patch])
plt.title('Accuracy of Page Ranks')
plt.ylabel('Error in % of power iteration values')
plt.xlabel('Random Walk Length')
plt.show()

difference = []
random_walk_lengths = [25, 50, 100]
for random_walk_length in random_walk_lengths:
    number_of_random_walks = 10
    while number_of_random_walks <= 500:
        number_of_random_walks += 50
        pr = IncrementalPersonalizedPageRank(graph, 0, number_of_random_walks, 0.05, random_walk_length)
        pr.initial_random_walks()
        page_ranks = pr.compute_personalized_page_ranks()
        page_ranks_2 = nx.pagerank(pr.graph, alpha=0.95, personalization={0: 1},
                                   max_iter=500, weight='weight')
        difference.append(np.linalg.norm(np.array(page_ranks.values()) - np.array(page_ranks_2.values())) /
                          np.linalg.norm(page_ranks_2.values()))
plt.plot(range(60, 510, 50), difference[0:9], 'r', range(60, 510, 50), difference[10:19], 'g',
         range(60, 510, 50), difference[20:29], 'y')
red_patch = mpatches.Patch(color='red', label='Random Walk Length: 25')
green_patch = mpatches.Patch(color='green', label='Random Walk Length: 50')
yellow_patch = mpatches.Patch(color='yellow', label='Random Walk Length: 100')
plt.legend(handles=[red_patch, green_patch, yellow_patch])
plt.title('Accuracy of Page Ranks')
plt.ylabel('Error in % of power iteration values')
plt.xlabel('Number of Random Walks')
plt.show()

difference = []
reset_probabilities = [0.05, 0.1, 0.15, 0.3, 0.5, 0.7, 0.9]
for reset_probability in reset_probabilities:
    number_of_random_walks = 10
    while number_of_random_walks <= 500:
        number_of_random_walks += 5
        pr = IncrementalPersonalizedPageRank2(graph, 0, number_of_random_walks, 0.05)
        pr.initial_random_walks()
        page_ranks = pr.compute_personalized_page_ranks()
        page_ranks_2 = nx.pagerank(pr.graph, alpha=0.95, personalization={0: 1},
                                   max_iter=500, weight='weight')

        difference.append(np.linalg.norm(np.array(page_ranks.values()) - np.array(page_ranks_2.values())) /
                          np.linalg.norm(page_ranks_2.values()))
plt.plot(range(15, 510, 5), difference[0:99], 'r', range(15, 510, 5), difference[99:198], 'g',
         range(15, 510, 5), difference[198:297], 'y', range(15, 510, 5), difference[297:396], 'b',
         range(15, 510, 5), difference[396:495], 'c')
red_patch = mpatches.Patch(color='red', label='Reset Probability: 0.05')
green_patch = mpatches.Patch(color='green', label='Reset Probability: 0.1')
yellow_patch = mpatches.Patch(color='yellow', label='Reset Probability: 0.15')
blue_patch = mpatches.Patch(color='blue', label='Reset Probability: 0.3')
cyan_patch = mpatches.Patch(color='cyan', label='Reset Probability: 0.5')
plt.legend(handles=[red_patch, green_patch, yellow_patch, blue_patch])
plt.title('Accuracy of Page Ranks')
plt.ylabel('Error in % of power iteration values')
plt.xlabel('Number of Random Walks')
plt.show()


difference = []
numbers_of_random_walks = [10, 100, 300]
for number_of_random_walks in numbers_of_random_walks:
    reset_probability = 0.05
    while reset_probability <= 0.95:
        pr = IncrementalPersonalizedPageRank2(graph, 0, number_of_random_walks, reset_probability)
        pr.initial_random_walks()
        page_ranks = pr.compute_personalized_page_ranks()
        page_ranks_2 = nx.pagerank(pr.graph, alpha=1-reset_probability, personalization={0: 1},
                                   max_iter=500, weight='weight')
        difference.append(np.linalg.norm(np.array(page_ranks.values()) - np.array(page_ranks_2.values())) /
                          np.linalg.norm(page_ranks_2.values()))
        reset_probability += 0.05
plt.plot(list(np.linspace(0.05, 0.9, 18)), difference[0:18], 'r',
         list(np.linspace(0.05, 0.9, 18)), difference[18:36], 'g',
         list(np.linspace(0.05, 0.9, 18)), difference[36:64], 'y',
         )
red_patch = mpatches.Patch(color='red', label='10 Random Walks')
green_patch = mpatches.Patch(color='green', label='100 Random Walks')
yellow_patch = mpatches.Patch(color='yellow', label='300 Random Walks')
plt.legend(handles=[red_patch, green_patch, yellow_patch])
plt.title('Accuracy of Page Ranks')
plt.ylabel('Error in % of power iteration values')
plt.xlabel('Reset Probability')
plt.show()
