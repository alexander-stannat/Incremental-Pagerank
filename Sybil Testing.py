""" The area under the ROC curve measures the overall quality of the ranking, i.e., the probability that a random
non-Sybil node  is  ranked  higher  than  a  random  Sybil. It  ranges from 0 to 1, with 0.5 indicating a random
ranking. An effective Sybil detection scheme should achieve a value > 0.5. Given a node ranked list, sliding
the pivot point regulates the trade-off between the two false rates. We set the pivot point based on a fixed value
for one false rate and compute the other false rate. We set the fixed false rate equal to 20%.  In the real
world, OSNs do not need a pivot point because none of the defenses so far can yield a binary Sybil/non-Sybil
classifier with an acceptable false positive rate. The ROC curve exhibits the change of the true positive rate with
the false positive rate as a pivot point moves along the ranked list: a node below the pivot point in the ranked
list is determined to be a Sybil; if the node is  actually  a  non-Sybil,  we  have  a  false  positive. """

from __future__ import division
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
from Page_Rank2 import IncrementalPersonalizedPageRank2
import matplotlib.patches as mpatches
import copy


random.seed(135)  # 7
honest_region = nx.DiGraph()
number_of_honest_nodes = 500
honest_nodes = range(number_of_honest_nodes)
reset_probabilities = [0.001, 0.005, 0.01, 0.05]

honest_region.add_nodes_from(honest_nodes)
for _ in range(4*number_of_honest_nodes):
    node_1 = random.choice(list(honest_region.nodes))
    node_2 = random.choice(list(set(honest_region.nodes) - {node_1}))
    if honest_region.has_edge(node_1, node_2) or honest_region.has_edge(node_2, node_1):
        continue
    else:
        weight = random.randint(1, 10)
        honest_region.add_weighted_edges_from([(node_1, node_2, weight)])

number_of_sybil_nodes = 1000
sybil_region = nx.DiGraph()
sybil_nodes = range(number_of_honest_nodes, number_of_honest_nodes + number_of_sybil_nodes)
sybil_region.add_nodes_from(sybil_nodes)
for _ in range(number_of_sybil_nodes):
    node_1 = random.choice(list(sybil_region.nodes))
    node_2 = random.choice(list(set(sybil_region.nodes) - {node_1}))
    if sybil_region.has_edge(node_1, node_2) or sybil_region.has_edge(node_2, node_1):
        continue
    else:
        weight = random.randint(1, 10)
        sybil_region.add_weighted_edges_from([(node_1, node_2, weight)])

node_color = []
for node in honest_region.nodes():
    node_color.append('green')
for node in sybil_region.nodes():
    node_color.append('blue')

initial_graph = nx.compose(honest_region, sybil_region)
# nx.draw_circular(graph, node_size=30, edge_width=0.0005, node_color=node_color, with_labels=True)
# plt.show()

area_ROC = []
false_positives = []
false_negatives = []
for reset_probability in reset_probabilities:
    graph = copy.deepcopy(initial_graph)
    for number_of_attack_edges in range(500):
        for _ in range(number_of_attack_edges):
            honest_node = random.choice(list(honest_region.nodes()))
            sybil_node = random.choice(list(sybil_region.nodes()))

            r = random.uniform(0, 1)
            if r < 0.5:
                graph.add_weighted_edges_from([(honest_node, sybil_node, random.randint(1, 10))])
            else:
                graph.add_weighted_edges_from([(sybil_node, honest_node, random.randint(1, 10))])

        #  nx.draw_circular(graph, node_size=30, edge_width=0.0005, node_color=node_color, with_labels=True)
        #  plt.show()

        #  print nx.shortest_path(graph, 501, 502)

        """for i in sybil_nodes:
            try:
                print nx.shortest_path(graph, 0, i)
            except nx.exception.NetworkXNoPath:
                print "No path between 0 and ", i"""

        pr = IncrementalPersonalizedPageRank2(graph, 0, 200, reset_probability)
        pr.initial_random_walks()
        page_ranks = pr.compute_personalized_page_ranks()
        truncated_page_ranks = {k: v for k, v in page_ranks.items() if v != 0}
        page_ranks_list = sorted(truncated_page_ranks.iteritems(), key=lambda (k, v): (v, k), reverse=True)
        print page_ranks_list
        ordered_nodes = list(zip(*page_ranks_list)[0])

        ROC_abscissa = []
        ROC_ordinate = []
        for i in range(1, len(ordered_nodes)+1):
            positives = ordered_nodes[:i]  # Non Sybils
            negatives = ordered_nodes[i:]  # Sybils
            ROC_abscissa.append(len(set(positives).intersection(set(sybil_region.nodes()))) / len(sybil_region.nodes()))
            ROC_ordinate.append(len(set(positives).intersection(set(honest_region.nodes()))) / len(honest_region.nodes()))

        # plt.plot(ROC_abscissa, ROC_ordinate)
        # plt.show()

        area_ROC.append(np.trapz(ROC_ordinate, ROC_abscissa))
        false_positives.append(len(list(set(ordered_nodes[:number_of_honest_nodes]).intersection(set(sybil_nodes)))) /
                               number_of_sybil_nodes)
        false_negatives.append(len(list(set(ordered_nodes[number_of_honest_nodes:]).intersection(set(honest_nodes)))) /
                               number_of_honest_nodes)


plt.plot(range(50), area_ROC[:50], 'r',
         range(50), area_ROC[50:100], 'g',
         range(50), area_ROC[100:150], 'b',
         range(50), area_ROC[150:200], 'y')
red_patch = mpatches.Patch(color='red', label='Reset Probability 0.1')
green_patch = mpatches.Patch(color='green', label='Reset Probability 0.3')
blue_patch = mpatches.Patch(color='blue', label='Reset Probability 0.5')
yellow_patch = mpatches.Patch(color='yellow', label='Reset Probability 0.7')
plt.legend(handles=[red_patch, green_patch, blue_patch, yellow_patch])
plt.xlabel("Number of Attack Edges")
plt.ylabel("Area under ROC Curve")
plt.title("Sybil Resistance of Page Rank")
plt.show()
print false_positives
print len(false_positives)
plt.plot(range(50), false_positives[:50], 'r',
         range(50), false_positives[50:100], 'g',
         range(50), false_positives[100:150], 'b',
         range(50), false_positives[150:200], 'y')
red_patch = mpatches.Patch(color='red', label='Reset Probability 0.1')
green_patch = mpatches.Patch(color='green', label='Reset Probability 0.3')
blue_patch = mpatches.Patch(color='blue', label='Reset Probability 0.5')
yellow_patch = mpatches.Patch(color='yellow', label='Reset Probability 0.7')
plt.legend(handles=[red_patch, green_patch, blue_patch, yellow_patch])
plt.xlabel("Number of Attack Edges")
plt.ylabel("Proportion of False Positives")
plt.title("Sybil Resistance of Page Rank")
plt.show()
print false_negatives
print len(false_negatives)
plt.plot(range(50), false_negatives[:50], 'r',
         range(50), false_negatives[50:100], 'g',
         range(50), false_negatives[100:150], 'b',
         range(50), false_negatives[150:200], 'y')
red_patch = mpatches.Patch(color='red', label='Reset Probability 0.1')
green_patch = mpatches.Patch(color='green', label='Reset Probability 0.3')
blue_patch = mpatches.Patch(color='blue', label='Reset Probability 0.5')
yellow_patch = mpatches.Patch(color='yellow', label='Reset Probability 0.7')
plt.legend(handles=[red_patch, green_patch, blue_patch, yellow_patch])
plt.xlabel("Number of Attack Edges")
plt.ylabel("Proportion of False Negatives")
plt.title("Sybil Resistance of Page Rank")
plt.show()
