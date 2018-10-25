"""
The code below opens the trustchain data set and and runs the Monte Carlo page rank algorithm on a graph generated
from all transactions blocks, where nodes correspond to peers and edge weights to net flows of data in between peers.
The execution of the entire code takes roughly 120 seconds. Loading the data set only needs to be done once. Thereafter
the page ranks are computed incrementally upon changes in the graph.
"""
from __future__ import division
from Open_Database2 import GraphReduction2
from Page_Rank2 import IncrementalPersonalizedPageRank2
import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import numpy as np
from Trust_GUI import Window
from PyQt5 import QtWidgets
import sys

"""
start_time = time.time()
file_path = "C:\\Users\\alexa\\Documents\\TU Delft\\Course material\\Other\\Blockchain\\Blockchain Lab\\Incremental Pagerank\\"
file_name = "trustchain"

gr = GraphReduction2(file_path, file_name)
gr.open_data_set()
graph = gr.generate_graph()
nx.draw_shell(graph, node_size=30, edge_width=1)
<<<<<<< HEAD
nx.draw_circular(graph, node_size=30)
=======
>>>>>>> c91ac3e... Initial Commit
plt.show()

node = random.choice(gr.nodes)
pr = IncrementalPersonalizedPageRank2(graph, node, 300, 0.05)
pr.initial_random_walks()
page_ranks = pr.compute_personalized_page_ranks()
page_ranks_2 = nx.pagerank(graph, alpha=0.95, personalization={node: 1},
                           max_iter=500, weight='weight')
print "Monte Carlo Pageranks: ", page_ranks.values()
print "Power Iteration Pageranks: ", page_ranks_2.values()
print np.linalg.norm(np.array(page_ranks.values()) - np.array(page_ranks_2.values())) / \
      np.linalg.norm(page_ranks_2.values())
<<<<<<< HEAD
print np.max(np.array(page_ranks.values()) - np.array(page_ranks_2.values()))
=======
>>>>>>> c91ac3e... Initial Commit

finish_time = time.time()

print finish_time - start_time, " Seconds"
"""

w = Window(1, 1, 1, 1)
w.place_window()

