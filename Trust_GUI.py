"""
The code below opens the trustchain database and runs the Monte Carlo PageRank algorithm on it's directed graph
determining the trustworthiness of the agents in the network.
"""

from __future__ import division
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx
import sys
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
import operator
from heapq import nlargest
import copy


class TrustGUI(QWidget):
    NumButtons = ['Show All Peers', 'Show Most Trusted Peer', 'Show Trustworthy Peers']

    def __init__(self, graph, main_node, page_ranks):
        super(TrustGUI, self).__init__()

        self.graph = graph
        self.page_ranks = page_ranks
        self.main_node = main_node
        self.setMouseTracking(True)

        self.initUI()

    def initUI(self):
        """

        :return:
        """

        """ Set Window Parameters """
        self.setGeometry(100, 100, 800, 600)
        self.center()
        self.setWindowTitle('Network Plot')
        self.setWindowIcon(QIcon('Tribler Logo.png'))


        """ Set Grid Layout """
        self.grid = QGridLayout()
        self.setLayout(self.grid)


        """ Create Actions for GUI window """
        exitAct = QAction('Exit Application', self)
        exitAct.setShortcut('Ctrl+W')
        exitAct.setStatusTip('Closes the Network Explorer')
        exitAct.triggered.connect(QApplication.instance().quit)


        """ Create Menubar at the top of the window """
        menubar = QMenuBar()
        self.grid.addWidget(menubar, 0, 0)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAct)


        """ Create Statusbar at the bottom of the window """
        statusbar = QStatusBar()
        self.grid.addWidget(statusbar, 9, 0)
        statusbar.showMessage("Ready")
        statusbar.show()


        """ Create Vertical Box of Buttons """
        buttonLayout = QVBoxLayout()
        self.createVerticalGroupBox()
        buttonLayout.addWidget(self.verticalGroupBox)


        """ Create Canvas for Network Display and Buttons"""
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.grid.addWidget(self.canvas, 0, 1, 9, 9)
        self.grid.addLayout(buttonLayout, 1, 0)


        """ Create Network Display """
        self.showgraph(self.main_node)


        """ Show Widget """
        self.show()


    def createVerticalGroupBox(self):
        self.verticalGroupBox = QGroupBox()
        layout = QVBoxLayout()
        for i in self.NumButtons:
            button = QPushButton(i)
            button.setObjectName(i)
            layout.addWidget(button)
            layout.setSpacing(10)
            self.verticalGroupBox.setLayout(layout)
            button.clicked.connect(self.submitCommand)
        return

    def submitCommand(self):
        eval('self.' + str(self.sender().objectName()).replace(" ", "") + '()')
        return

    def ShowMostTrustedPeer(self):
        self.page_ranks_of_subgraph = {node: self.page_ranks[node] for node in self.sub_graph.nodes()}
        del self.page_ranks_of_subgraph[self.main_node]
        self.most_trusted_node = max(self.page_ranks_of_subgraph.iteritems(), key=operator.itemgetter(1))[0]
        del self.page_ranks_of_subgraph[self.most_trusted_node]

        self.node_color_trusted = []
        self.node_color_untrusted = []

        for node in self.sub_graph.nodes():
            if node in self.page_ranks_of_subgraph.keys():
                if self.page_ranks[node] < 0.0001:
                    self.node_color_untrusted.append('red')
                if 0.0001 < self.page_ranks[node] < 0.0005:
                    self.node_color_untrusted.append('yellow')
                if self.page_ranks[node] > 0.0005:
                    self.node_color_untrusted.append('green')
            else:
                if self.page_ranks[node] < 0.0001:
                    self.node_color_trusted.append('red')
                if 0.0001 < self.page_ranks[node] < 0.0005:
                    self.node_color_trusted.append('yellow')
                if self.page_ranks[node] > 0.0005:
                    self.node_color_trusted.append('green')

        self.figure.clf()
        self.canvas.draw_idle()

        plt.title('Tribler Network', size=15)
        plt.axis('off')

        nx.draw_networkx_nodes(self.sub_graph, pos=self.pos, nodelist=[self.main_node, self.most_trusted_node],
                               node_size=50, width=0.05, node_color=self.node_color_trusted)
        nx.draw_networkx_nodes(self.sub_graph, pos=self.pos, nodelist=self.page_ranks_of_subgraph.keys(), node_size=50,
                               width=0.05, node_color=self.node_color_untrusted, alpha=0.1)
        nx.draw_networkx_edges(self.sub_graph, pos=self.pos, edgelist=[(self.main_node, self.most_trusted_node)], width=0.2)
        nx.draw_networkx_edges(self.sub_graph, pos=self.pos, edgelist=self.sub_graph.edges(), width=0.05, alpha=0.1)

    def ShowTrustworthyPeers(self):
        self.page_ranks_of_subgraph = {node: self.page_ranks[node] for node in self.sub_graph.nodes()}
        del self.page_ranks_of_subgraph[self.main_node]
        self.most_trusted_nodes = nlargest(10, self.page_ranks_of_subgraph)

        for node in self.most_trusted_nodes:
            del self.page_ranks_of_subgraph[node]

        self.node_color_trusted = []
        self.node_color_untrusted = []

        for node in self.sub_graph.nodes():
            if node in self.page_ranks_of_subgraph.keys():
                if self.page_ranks[node] < 0.0001:
                    self.node_color_untrusted.append('red')
                if 0.0001 < self.page_ranks[node] < 0.0005:
                    self.node_color_untrusted.append('yellow')
                if self.page_ranks[node] > 0.0005:
                    self.node_color_untrusted.append('green')
            else:
                if self.page_ranks[node] < 0.0001:
                    self.node_color_trusted.append('red')
                if 0.0001 < self.page_ranks[node] < 0.0005:
                    self.node_color_trusted.append('yellow')
                if self.page_ranks[node] > 0.0005:
                    self.node_color_trusted.append('green')

        self.figure.clf()
        self.canvas.draw_idle()

        plt.title('Tribler Network', size=15)
        plt.axis('off')

        nodelist = list(set(self.most_trusted_nodes).union({self.main_node}))
        nx.draw_networkx_nodes(self.sub_graph, pos=self.pos, nodelist=nodelist,
                               node_size=50, width=0.05, node_color=self.node_color_trusted)

        nx.draw_networkx_nodes(self.sub_graph, pos=self.pos, nodelist=self.page_ranks_of_subgraph.keys(), node_size=50,
                               width=0.05, node_color=self.node_color_untrusted, alpha=0.1)
        #nx.
        return

    def ShowAllPeers(self):
        self.showgraph(self.main_node)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showgraph(self, main_node):
        main_node_neighbours = list(set(nx.DiGraph.successors(self.graph, main_node)).union(
            set(nx.DiGraph.predecessors(self.graph, main_node))))

        neighbours_of_neighbours = dict()
        all_neighbours_of_neighbours = []

        for j in range(len(main_node_neighbours)):
            node_neighbours = []
            node_neighbours.extend(nx.DiGraph.successors(self.graph, main_node_neighbours[j]))
            node_neighbours.extend(nx.DiGraph.predecessors(self.graph, main_node_neighbours[j]))
            node_neighbours.remove(main_node)
            node_neighbours = list(set(node_neighbours) - set(main_node_neighbours))

            for node in node_neighbours:
                if node in all_neighbours_of_neighbours:
                    node_neighbours.remove(node)
                else:
                    continue

            all_neighbours_of_neighbours.extend(node_neighbours)
            neighbours_of_neighbours[main_node_neighbours[j]] = node_neighbours

        self.sub_graph = nx.DiGraph.subgraph(self.graph, list(set(main_node_neighbours).union({main_node}).union(all_neighbours_of_neighbours)))
        plt.title('Tribler Network', size=15)
        plt.axis('off')

        self.pos = nx.spring_layout(self.sub_graph, center=np.array([0, 0]), scale=20)
        self.pos[main_node] = np.array([0, 0])

        angle_first_circle = (2*np.pi) / len(main_node_neighbours)
        angle_second_circle = dict()

        i = 0
        for node in main_node_neighbours:
            self.pos[node] = np.array([np.cos(angle_first_circle * i) * 20, np.sin(angle_first_circle * i) * 20])
            try:
                angle_second_circle[node] = angle_first_circle/len(neighbours_of_neighbours[node])
            except ZeroDivisionError:
                angle_second_circle[node] = None
            i += 1

        i = 0
        for node1 in neighbours_of_neighbours.keys():
            j = 0
            for node2 in neighbours_of_neighbours[node1]:
                # pos[node2] = np.array([np.cos(angle_second_circle[node1] * j + angle_first_circle * i - angle_first_circle / 2) * 20, np.sin(angle_second_circle[node1] * j + angle_first_circle * i - angle_first_circle / 2) * 20])
                self.pos[node2] = np.array(
                    [np.cos(angle_second_circle[node1] * j + angle_first_circle * i - angle_first_circle / 2) * 40,
                     np.sin(angle_second_circle[node1] * j + angle_first_circle * i - angle_first_circle / 2) * 40])
                j += 1
            i += 1

        self.node_color = []
        for node in self.sub_graph.nodes():
            if self.page_ranks[node] < 0.0001:
                self.node_color.append('red')
            if 0.0001 < self.page_ranks[node] < 0.0005:
                self.node_color.append('yellow')
            if self.page_ranks[node] > 0.0005:
                self.node_color.append('green')

        self.figure.clf()
        self.canvas.draw_idle()

        labels = {}
        labels[self.main_node] = r'you'
        self.pos[main_node] = np.array([0, 0])
        nx.draw(self.sub_graph, with_labels=True, labels=labels, pos=self.pos, node_color=self.node_color, node_size=50, width=0.05)
