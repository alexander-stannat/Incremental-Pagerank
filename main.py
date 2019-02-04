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
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Trust_GUI import TrustGUI
from Trust_GUI_Practice import Window,StatusBar, Clickmenu
from PyQt5.QtWidgets import QWidget, QApplication
import pickle
import sys


start_time = time.time()
file_path = "C:\\Users\\alexa\\Documents\\TU Delft\\Course material\\Other\\Blockchain\\Blockchain Lab\\Incremental Pagerank\\"
file_name = "trustchain"

gr = GraphReduction2(file_path, file_name)
gr.open_data_set()
graph = gr.generate_graph()

main_node = random.choice(list(graph.nodes()))
pr = IncrementalPersonalizedPageRank2(graph, main_node, 300, 0.05)
pr.initial_random_walks()
page_ranks = pr.compute_personalized_page_ranks()
page_ranks_2 = nx.pagerank(graph, alpha=0.95, personalization={main_node: 1},
                           max_iter=500, weight='weight')
print "Monte Carlo Pageranks: ", page_ranks.values()
print "Power Iteration Pageranks: ", page_ranks_2.values()
print np.linalg.norm(np.array(page_ranks.values()) - np.array(page_ranks_2.values())) / \
      np.linalg.norm(page_ranks_2.values())

finish_time = time.time()
print finish_time - start_time, " Seconds" 

"""
dataset = [graph, main_node, page_ranks]
outputFile = 'test.data'
fw = open(outputFile, 'wb')
pickle.dump(dataset, fw)
fw.close()


inputFile = 'test.data'
fd = open(inputFile, 'rb')
dataset = pickle.load(fd)

graph = dataset[0] 
main_node = dataset[1]
page_ranks = dataset[2]
"""

app = QApplication(sys.argv)
trustgui = TrustGUI(graph, main_node, page_ranks)
sys.exit(app.exec_())


