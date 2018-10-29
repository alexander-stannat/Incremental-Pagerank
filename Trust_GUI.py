"""
The code below opens the trustchain database and runs the Monte Carlo PageRank algorithm on it's directed graph
determining the trustworthiness of the agents in the network.
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx
import sys
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class TrustGraph(QWidget):
    NumButtons = ['Show Neighbourhood', 'Most Trusted Peer', 'Most Likely Path']

    def __init__(self, graph):
        super(TrustGraph, self).__init__()

        self.graph = graph
        self.subgraph = nx.DiGraph()
        # self.main_node = main_node

        font = QFont()
        font.setPointSize(16)

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.center()
        self.setWindowTitle('Network Plot')
        self.setWindowIcon(QIcon('Tribler Logo.png'))

        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.createVerticalGroupBox()

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.verticalGroupBox)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.grid.addWidget(self.canvas, 0, 1, 9, 9)
        self.grid.addLayout(buttonLayout, 0, 0)

        self.main_node = list(self.graph.nodes())[0]

        node_color = []
        for node in self.graph.nodes():
            if node == self.main_node:
                node_color.append('red')
            else:
                node_color.append('blue')

        nx.draw_networkx(self.graph, node_color=node_color)

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

    def ShowNeighbourhood(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.grid.addWidget(self.canvas, 0, 1, 9, 9)
        self.subgraph = self.graph.subgraph(list(set(self.main_node).union(set(self.graph.neighbors(self.main_node)))))
        nx.draw_networkx(self.subgraph)
        # self.show()
        return

    def MostTrustedPeer(self):

        print 2

    def MostLikelyPath(self):

        print 3

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
