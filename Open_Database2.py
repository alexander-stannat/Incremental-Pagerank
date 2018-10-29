"""
The code below opens the multi-chain database and generates a graph of nodes corresponding to peers in the network
and edges representing the flow of data in between peers
"""
import sqlite3
import networkx as nx
from Encode import decode
import copy


class GraphReduction2(object):
    """
    Class to open the multichain data set file consisting of tables, comprising the columns: type,
    tx (a dictionary containing the amount of up- and downloaded data), public_key, sequence_number_requester,
    public key responder (link public key), link sequence number, previous hash, signature, block timestamp,
    insert time and block hash

    A directed graph is then generated with nodes corresponding to the public_key of peers in the network and edges
    representing interactions between individual peers. The weight of an edge connecting to peers is determined by
    the net flow of data in between these peers. The direction of an edge is determined by the sign of the net flow,
    i.e. if a has transferred 3GB to b and b has transferred 1GB to a, then the graph will have a directed edge from
    a to b of weight 2GB.
    """

    def __init__(self, file_path, file_name):
        """
        Initializes Graph Reduction Class
        :param file_path: Path of database file
        :param file_name: Name of database file
        """
        self.file_path = file_path
        self.file_name = file_name
        self.graph = nx.DiGraph()
        self.blocks = []
        self.nodes = set()
        self.edges = dict()

    def open_data_set(self):
        """
        Accesses the trustchain data set and opens all rows. Then a graph is generated from all rows with nodes
        corresponding to public keys and edges corresponding to transactions.
        """
        conn = sqlite3.connect(self.file_path + self.file_name + ".db")
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM blocks""")
        self.blocks = iter(cursor.fetchall())
        for block in self.blocks:
            self.nodes.update([str(block[2]).encode('hex'), str(block[4]).encode('hex')])
            if decode(str(block[1]))[1].keys() == ["down", "total_down", "up", "total_up"]:
                if (str(block[2]).encode('hex'), str(block[4]).encode('hex')) in self.edges.keys():
                    self.edges[(str(block[2]).encode('hex'), str(block[4]).encode('hex'))] += \
                        decode(str(block[1]))[1]["down"] - decode(str(block[1]))[1]["up"]
                    if self.edges[(str(block[2]).encode('hex'), str(block[4]).encode('hex'))] < 0:
                        self.edges[(str(block[4]).encode('hex'), str(block[2]).encode('hex'))] = -\
                            self.edges[(str(block[2]).encode('hex'), str(block[4]).encode('hex'))]
                        del self.edges[(str(block[2]).encode('hex'), str(block[4]).encode('hex'))]
                elif (str(block[4]).encode('hex'), str(block[2]).encode('hex')) in self.edges.keys():
                    self.edges[(str(block[4]).encode('hex'), str(block[2]).encode('hex'))] += \
                        decode(str(block[1]))[1]["up"] - decode(str(block[1]))[1]["down"]
                    if self.edges[(str(block[4]).encode('hex'), str(block[2]).encode('hex'))] < 0:
                        self.edges[(str(block[2]).encode('hex'), str(block[4]).encode('hex'))] = -\
                            self.edges[(str(block[4]).encode('hex'), str(block[2]).encode('hex'))]
                        del self.edges[(str(block[4]).encode('hex'), str(block[2]).encode('hex'))]
                else:
                    if decode(str(block[1]))[1]["down"] - decode(str(block[1]))[1]["up"] >= 0:
                        self.edges[(str(block[2]).encode('hex'), str(block[4]).encode('hex'))] = \
                            decode(str(block[1]))[1]["down"] - decode(str(block[1]))[1]["up"]
                    elif decode(str(block[1]))[1]["down"] - decode(str(block[1]))[1]["up"] < 0:
                        self.edges[(str(block[4]).encode('hex'), str(block[2]).encode('hex'))] = \
                            decode(str(block[1]))[1]["up"] - decode(str(block[1]))[1]["down"]
                    if decode(str(block[1]))[1]["up"] - decode(str(block[1]))[1]["down"] >= 0:
                        self.edges[(str(block[2]).encode('hex'), str(block[4]).encode('hex'))] = \
                            decode(str(block[1]))[1]["up"] - decode(str(block[1]))[1]["down"]
                    elif decode(str(block[1]))[1]["up"] - decode(str(block[1]))[1]["down"] < 0:
                        self.edges[(str(block[4]).encode('hex'), str(block[2]).encode('hex'))] = \
                            decode(str(block[1]))[1]["down"] - decode(str(block[1]))[1]["up"]

        self.nodes = list(self.nodes)
        self.edges = iter(zip(self.edges.keys(), self.edges.values()))
        self.edges = iter(edge[0] + (edge[1],) for edge in self.edges)
        return

    def generate_graph(self):
        self.graph.add_nodes_from(self.nodes)
        self.graph.add_weighted_edges_from(list(self.edges))
        return self.graph
