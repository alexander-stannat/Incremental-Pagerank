"""
The code in this file computes the PageRanks using the Monte Carlo algorithm.
"""

import networkx as nx
import random
from numpy import cumsum, array


class IncrementalPersonalizedPageRank(object):
    """
    Class to incrementally compute the personalized page ranks of a graph from the perspective of a predetermined
    node in the graph.

    Page rank is an algorithm with which nodes in a directed graph are ranked by their respective importance.
    Personalized page rank is an alternate version of page rank where the ranks of nodes are determined by their
    distance from a given seed node.
    Usually, the page ranks in a network are computed using an iterative procedure called the power iteration.
    In this class the page ranks are computed using the monte carlo method, whereby a number of random walks of
    predetermined lengths originate from the seed node and walk along the edges through the graph. They jump back
    to the seed node with a given probability at every step and the walk is terminated once it reaches a certain
    length. If a random walk reaches a "dangling node", i.e. a node with no outgoing edges it is reset as well.
    A vector of visit times is computed containing the number of times the random walk passes through the individual
    nodes and the page rank is given by the visit times divided by the accumulated visit times of all nodes in the
    graph.
    The personalised page rank given below is incremental, meaning that it can be recomputed every time the underlying
    graph structure is modified. In order to recompute the page ranks, one doesn't have to recompute the entire set
    of random walks through the graph. Instead, the given set of random walks is modified. The idea behind this is
    that a given random walk does not pass through every single edge. Only random walks that reach a node for which
    the outgoing edges have been modified, i.e. an edge is added or removed, or the weight of an edge is changed,
    need to be recomputed, starting from the first node for which such changes have occurred.
    """

    def __init__(self, graph, node, number_of_random_walks, reset_probability, random_walk_length):
        """
        Initializes the incremental personalized page rank class by determining the graph, the seed node, the number
        of random walks, the reset probability and the length of each random walk.

        :type node: The seed node at which all random walks begin
        :param graph: The graph for which the incremental page rank is computed
        :param number_of_random_walks: The number of random walks starting at the seed node
        :param reset_probability: The probability with which a random walk jumps back to the seed node
        :param random_walk_length: The number of nodes each random walk goes through before it's terminated
        """
        self.graph = graph
        self.node = node
        self.number_of_random_walks = number_of_random_walks
        self.reset_probability = reset_probability
        self.random_walk_length = random_walk_length

        self.random_walks = list()
        self.added_edges = list()
        self.removed_edges = list()

    def initial_random_walks(self):
        """
        Initiates the random_walk_from_node function starting from the seed node, number_of_random_walks times
        """
        while len(self.random_walks) < self.number_of_random_walks:
            self.regular_random_walk(self.node)
        return

    def regular_random_walk(self, node):
        """
        Computes a random walk starting from node and appending all nodes it passes though to the list random_walk
        :param node: The node at which the random walk begins
        """
        random_walk = [node]
        while len(random_walk) < self.random_walk_length:
            c = random.uniform(0, 1)
            if len(list(self.graph.neighbors(random_walk[-1]))) > 0 and c > self.reset_probability:
                current_node = random_walk[-1]
                current_neighbors = list(self.graph.neighbors(current_node))
                current_edge_weights = array(
                    [self.graph[current_node][neighbor]['weight'] for neighbor in current_neighbors])
                cumulated_edge_weights = cumsum(current_edge_weights)
                if cumulated_edge_weights[-1] == 0:
                    random_walk.append(self.node)
                    continue
                random_id = list(
                    cumulated_edge_weights < (random.uniform(0, 1) * cumulated_edge_weights[-1])).index(
                    False)
                next_node = current_neighbors[random_id]
                random_walk.append(next_node)
            else:
                random_walk.append(self.node)
        self.random_walks.append(random_walk)
        return

    def add_random_walk(self, previous_random_walk):
        """
        Takes a given random walk segment and computes random walk of length random_walk_length starting at the final
        node in the previous random walk. The idea is that once the graph is modified some random walks will be
        recomputed starting at a given node in the graph.
        :param previous_random_walk: A random walk segment which is not as long as random_walk_length
        """
        random_walk = previous_random_walk
        while len(random_walk) < self.random_walk_length:
            c = random.uniform(0, 1)
            if len(list(self.graph.neighbors(random_walk[-1]))) > 0 and c > self.reset_probability:
                current_node = random_walk[-1]
                current_neighbors = list(self.graph.neighbors(current_node))
                current_edge_weights = array(
                    [self.graph[current_node][neighbor]['weight'] for neighbor in current_neighbors])
                cumulated_current_edge_weights = cumsum(current_edge_weights)
                if cumulated_current_edge_weights[-1] == 0:
                    random_walk.append(self.node)
                    continue
                random_id = list(
                    cumulated_current_edge_weights < (random.uniform(0, 1) * cumulated_current_edge_weights[-1])).index(
                    False)
                next_node = current_neighbors[random_id]
                random_walk.append(next_node)
            else:
                random_walk.append(self.node)
        self.random_walks.append(random_walk)
        return

    def compute_personalized_page_ranks(self):
        """
        Determines the personalized page ranks based the random walks in the list random_walks
        :return: A dictionary of nodes and corresponding page ranks
        """
        zeros = [0 for _ in range(len(list(self.graph.nodes)))]
        page_ranks = dict(zip(list(self.graph.nodes), zeros))
        visit_times = dict(zip(list(self.graph.nodes), zeros))
        nodes_in_random_walks = []
        for random_walk in self.random_walks:
            nodes_in_random_walks.extend(random_walk)
        for node in self.graph.nodes:
            visit_times[node] = nodes_in_random_walks.count(node)
        for node in self.graph.nodes:
            try:
                page_ranks[node] = float(visit_times[node]) / sum(visit_times.values())
            except ZeroDivisionError:
                print "List of visit times is empty..."
        return page_ranks

    def add_edge(self, source, destination, weight):
        """
        Adds an edge to the graph. Then adds the edge to the list added_edges
        :param source: source node
        :param destination: destination node
        :param weight: weight of the edge
        """
        if weight == 0 or source not in self.graph or destination not in self.graph:
            return
        if self.graph.has_edge(source, destination):
            self.add_weight_to_edge(source, destination, weight)
        elif self.graph.has_edge(destination, source):
            self.add_weight_to_edge(destination, source, -weight)
        else:
            if weight > 0:
                edge = (source, destination, weight)
            elif weight < 0:
                edge = (destination, source, -weight)
            self.graph.add_weighted_edges_from([edge])
            self.added_edges.append(edge)

    def add_weight_to_edge(self, source, destination, weight):
        """
        Takes an existing edge and updates its weight. Then adds the edge to the list added_edges
        :param source: source node of the edge
        :param destination: destination node of the edge
        :param weight: weight added to the edge
        """
        if weight == 0:
            return
        if self.graph.has_edge(source, destination):
            self.graph[source][destination]['weight'] += weight
            if self.graph[source][destination]['weight'] < 0:
                edge = (destination, source, -self.graph[source][destination]['weight'])
                self.graph.remove_edge(source, destination)
                self.graph.add_weighted_edges_from([edge])
                self.removed_edges.append((source, destination))
                self.added_edges.append(edge)
            elif self.graph[source][destination]['weight'] > 0:
                edge = (source, destination, self.graph[source][destination]['weight'])
                self.graph.remove_edge(source, destination)
                self.graph.add_weighted_edges_from([edge])
                self.added_edges.append(edge)
            elif self.graph[source][destination]['weight'] == 0:
                self.graph.remove_edge(source, destination)
                self.removed_edges.append((source, destination))

        elif self.graph.has_edge(destination, source):
            self.graph[destination][source]['weight'] -= weight
            if self.graph[destination][source]['weight'] < 0:
                edge = (source, destination, -self.graph[destination][source]['weight'])
                self.graph.remove_edge(destination, source)
                self.graph.add_weighted_edges_from([edge])
                self.added_edges.append(edge)
                self.removed_edges.append((destination, source))
            elif self.graph[destination][source]['weight'] > 0:
                edge = (destination, source, self.graph[destination][source]['weight'])
                self.graph.remove_edge(destination, source)
                self.graph.add_weighted_edges_from([edge])
                self.added_edges.append(edge)
            elif self.graph[destination][source]['weight'] == 0:
                self.graph.remove_edge(destination, source)
                self.removed_edges.append((destination, source))
        else:
            self.add_edge(source, destination, weight)
        return

    def remove_edge(self, source, destination):
        """
        Removes an edge from the graph and adds it to the list added_edges
        :param source: source node of the edge
        :param destination: destination node of the edge
        """
        if self.graph.has_edge(source, destination):
            edge = (source, destination)
            self.graph.remove_edge(source, destination)
            self.removed_edges.append(edge)
        elif self.graph.has_edge(destination, source):
            edge = (destination, source)
            self.graph.remove_edge(destination, source)
            self.removed_edges.append(edge)
        return

    def add_node(self, node):
        """
        Adds a node to the graph
        :param node: Node that is to be added
        """
        if node not in self.graph.nodes:
            self.graph.add_node(node)
        else:
            print "node already in graph"
        return

    def remove_node(self, node):
        """
        Removes a node from the graph
        :param node: node that is to be removed
        """
        if node in self.graph.nodes:
            for predecessor in self.graph.predecessors(node):
                if (predecessor, node) not in self.removed_edges:
                    self.removed_edges.append((predecessor, node))
                if (predecessor, node) in self.added_edges:
                    self.added_edges.remove((predecessor, node))
            for successor in self.graph.successors(node):
                if (node, successor) in self.added_edges:
                    self.added_edges.remove((node, successor))
                if (node, successor) not in self.removed_edges:
                    self.removed_edges.append((node, successor))
        for edge in reversed(self.removed_edges):
            if edge[0] == node:
                self.removed_edges.remove(edge)
        for edge in reversed(self.added_edges):
            if edge[0] == node:
                self.added_edges.remove(edge)

            self.graph.remove_node(node)
        return

    """def update_graph(self, new_graph):
        
        Takes a modification of the current graph and updates the lists added_edges and removed_edges
        :param new_graph: Modified version of the original graph
        
        old_edges = nx.get_edge_attributes(self.graph, 'weight').items()
        new_edges = nx.get_edge_attributes(new_graph, 'weight').items()
        for edge in list(set(new_edges) - set(old_edges)):
            self.add_edge(edge[0][0], edge[0][1], edge[1])"""

    def update_random_walks(self):
        """
        Takes the lists added_edges and removed_edges and recomputes all random walks that have traversed these
        edges, starting from their respective source nodes. The new random walks then replace the old ones in the
        list random_walks. Finally the edges are removed from the lists added_edges and removed_edges
        """
        for edge in reversed(self.added_edges):
            self.added_edges.remove(edge)
            random_walks_to_change = [random_walk for random_walk in self.random_walks if edge[0] in random_walk]
            for random_walk in random_walks_to_change:
                self.random_walks.remove(random_walk)
                del random_walk[random_walk.index(edge[0])+1:]
                self.add_random_walk(random_walk)

        for edge in reversed(self.removed_edges):
            self.removed_edges.remove(edge)
            random_walks_to_change = [random_walk for random_walk in self.random_walks if edge[0] in random_walk]
            for random_walk in random_walks_to_change:
                self.random_walks.remove(random_walk)
                del random_walk[random_walk.index(edge[0]) + 1:]
                self.add_random_walk(random_walk)
        return














"""
The code in this file computes the PageRanks using the Monte Carlo algorithm.
"""

import networkx as nx
import random
from numpy import cumsum, array


class IncrementalPersonalizedPageRank(object):
    """
    Class to incrementally compute the personalized page ranks of a graph from the perspective of a predetermined
    node in the graph.

    Page rank is an algorithm with which nodes in a directed graph are ranked by their respective importance.
    Personalized page rank is an alternate version of page rank where the ranks of nodes are determined by their
    distance from a given seed node.
    Usually, the page ranks in a network are computed using an iterative procedure called the power iteration.
    In this class the page ranks are computed using the monte carlo method, whereby a number of random walks of
    predetermined lengths originate from the seed node and walk along the edges through the graph. They jump back
    to the seed node with a given probability at every step and the walk is terminated once it reaches a certain
    length. If a random walk reaches a "dangling node", i.e. a node with no outgoing edges it is reset as well.
    A vector of visit times is computed containing the number of times the random walk passes through the individual
    nodes and the page rank is given by the visit times divided by the accumulated visit times of all nodes in the
    graph.
    The personalised page rank given below is incremental, meaning that it can be recomputed every time the underlying
    graph structure is modified. In order to recompute the page ranks, one doesn't have to recompute the entire set
    of random walks through the graph. Instead, the given set of random walks is modified. The idea behind this is
    that a given random walk does not pass through every single edge. Only random walks that reach a node for which
    the outgoing edges have been modified, i.e. an edge is added or removed, or the weight of an edge is changed,
    need to be recomputed, starting from the first node for which such changes have occurred.
    """

    def __init__(self, graph, node, number_of_random_walks, reset_probability, random_walk_length):
        """
        Initializes the incremental personalized page rank class by determining the graph, the seed node, the number
        of random walks, the reset probability and the length of each random walk.

        :type node: The seed node at which all random walks begin
        :param graph: The graph for which the incremental page rank is computed
        :param number_of_random_walks: The number of random walks starting at the seed node
        :param reset_probability: The probability with which a random walk jumps back to the seed node
        :param random_walk_length: The number of nodes each random walk goes through before it's terminated
        """
        self.graph = graph
        self.node = node
        self.number_of_random_walks = number_of_random_walks
        self.reset_probability = reset_probability
        self.random_walk_length = random_walk_length

        self.random_walks = list()
        self.added_edges = list()
        self.removed_edges = list()

    def initial_random_walks(self):
        """
        Initiates the random_walk_from_node function starting from the seed node, number_of_random_walks times
        """
        while len(self.random_walks) < self.number_of_random_walks:
            self.regular_random_walk(self.node)
        return

    def regular_random_walk(self, node):
        """
        Computes a random walk starting from node and appending all nodes it passes though to the list random_walk
        :param node: The node at which the random walk begins
        """
        random_walk = [node]
        while len(random_walk) < self.random_walk_length:
            c = random.uniform(0, 1)
            if len(list(self.graph.neighbors(random_walk[-1]))) > 0 and c > self.reset_probability:
                current_node = random_walk[-1]
                current_neighbors = list(self.graph.neighbors(current_node))
                current_edge_weights = array(
                    [self.graph[current_node][neighbor]['weight'] for neighbor in current_neighbors])
                cumulated_edge_weights = cumsum(current_edge_weights)
                if cumulated_edge_weights[-1] == 0:
                    random_walk.append(self.node)
                    continue
                random_id = list(
                    cumulated_edge_weights < (random.uniform(0, 1) * cumulated_edge_weights[-1])).index(
                    False)
                next_node = current_neighbors[random_id]
                random_walk.append(next_node)
            else:
                random_walk.append(self.node)
        self.random_walks.append(random_walk)
        return

    def add_random_walk(self, previous_random_walk):
        """
        Takes a given random walk segment and computes random walk of length random_walk_length starting at the final
        node in the previous random walk. The idea is that once the graph is modified some random walks will be
        recomputed starting at a given node in the graph.
        :param previous_random_walk: A random walk segment which is not as long as random_walk_length
        """
        random_walk = previous_random_walk
        while len(random_walk) < self.random_walk_length:
            c = random.uniform(0, 1)
            if len(list(self.graph.neighbors(random_walk[-1]))) > 0 and c > self.reset_probability:
                current_node = random_walk[-1]
                current_neighbors = list(self.graph.neighbors(current_node))
                current_edge_weights = array(
                    [self.graph[current_node][neighbor]['weight'] for neighbor in current_neighbors])
                cumulated_current_edge_weights = cumsum(current_edge_weights)
                if cumulated_current_edge_weights[-1] == 0:
                    random_walk.append(self.node)
                    continue
                random_id = list(
                    cumulated_current_edge_weights < (random.uniform(0, 1) * cumulated_current_edge_weights[-1])).index(
                    False)
                next_node = current_neighbors[random_id]
                random_walk.append(next_node)
            else:
                random_walk.append(self.node)
        self.random_walks.append(random_walk)
        return

    def compute_personalized_page_ranks(self):
        """
        Determines the personalized page ranks based the random walks in the list random_walks
        :return: A dictionary of nodes and corresponding page ranks
        """
        zeros = [0 for _ in range(len(list(self.graph.nodes)))]
        page_ranks = dict(zip(list(self.graph.nodes), zeros))
        visit_times = dict(zip(list(self.graph.nodes), zeros))
        nodes_in_random_walks = []
        for random_walk in self.random_walks:
            nodes_in_random_walks.extend(random_walk)
        for node in self.graph.nodes:
            visit_times[node] = nodes_in_random_walks.count(node)
        for node in self.graph.nodes:
            try:
                page_ranks[node] = float(visit_times[node]) / sum(visit_times.values())
            except ZeroDivisionError:
                print "List of visit times is empty..."
        return page_ranks

    def add_edge(self, source, destination, weight):
        """
        Adds an edge to the graph. Then adds the edge to the list added_edges
        :param source: source node
        :param destination: destination node
        :param weight: weight of the edge
        """
        if weight == 0 or source not in self.graph or destination not in self.graph:
            return
        if self.graph.has_edge(source, destination):
            self.add_weight_to_edge(source, destination, weight)
        elif self.graph.has_edge(destination, source):
            self.add_weight_to_edge(destination, source, -weight)
        else:
            if weight > 0:
                edge = (source, destination, weight)
            elif weight < 0:
                edge = (destination, source, -weight)
            self.graph.add_weighted_edges_from([edge])
            self.added_edges.append(edge)

    def add_weight_to_edge(self, source, destination, weight):
        """
        Takes an existing edge and updates its weight. Then adds the edge to the list added_edges
        :param source: source node of the edge
        :param destination: destination node of the edge
        :param weight: weight added to the edge
        """
        if weight == 0:
            return
        if self.graph.has_edge(source, destination):
            self.graph[source][destination]['weight'] += weight
            if self.graph[source][destination]['weight'] < 0:
                edge = (destination, source, -self.graph[source][destination]['weight'])
                self.graph.remove_edge(source, destination)
                self.graph.add_weighted_edges_from([edge])
                self.removed_edges.append((source, destination))
                self.added_edges.append(edge)
            elif self.graph[source][destination]['weight'] > 0:
                edge = (source, destination, self.graph[source][destination]['weight'])
                self.graph.remove_edge(source, destination)
                self.graph.add_weighted_edges_from([edge])
                self.added_edges.append(edge)
            elif self.graph[source][destination]['weight'] == 0:
                self.graph.remove_edge(source, destination)
                self.removed_edges.append((source, destination))

        elif self.graph.has_edge(destination, source):
            self.graph[destination][source]['weight'] -= weight
            if self.graph[destination][source]['weight'] < 0:
                edge = (source, destination, -self.graph[destination][source]['weight'])
                self.graph.remove_edge(destination, source)
                self.graph.add_weighted_edges_from([edge])
                self.added_edges.append(edge)
                self.removed_edges.append((destination, source))
            elif self.graph[destination][source]['weight'] > 0:
                edge = (destination, source, self.graph[destination][source]['weight'])
                self.graph.remove_edge(destination, source)
                self.graph.add_weighted_edges_from([edge])
                self.added_edges.append(edge)
            elif self.graph[destination][source]['weight'] == 0:
                self.graph.remove_edge(destination, source)
                self.removed_edges.append((destination, source))
        else:
            self.add_edge(source, destination, weight)
        return

    def remove_edge(self, source, destination):
        """
        Removes an edge from the graph and adds it to the list added_edges
        :param source: source node of the edge
        :param destination: destination node of the edge
        """
        if self.graph.has_edge(source, destination):
            edge = (source, destination)
            self.graph.remove_edge(source, destination)
            self.removed_edges.append(edge)
        elif self.graph.has_edge(destination, source):
            edge = (destination, source)
            self.graph.remove_edge(destination, source)
            self.removed_edges.append(edge)
        return

    def add_node(self, node):
        """
        Adds a node to the graph
        :param node: Node that is to be added
        """
        if node not in self.graph.nodes:
            self.graph.add_node(node)
        else:
            print "node already in graph"
        return

    def remove_node(self, node):
        """
        Removes a node from the graph
        :param node: node that is to be removed
        """
        if node in self.graph.nodes:
            for predecessor in self.graph.predecessors(node):
                if (predecessor, node) not in self.removed_edges:
                    self.removed_edges.append((predecessor, node))
                if (predecessor, node) in self.added_edges:
                    self.added_edges.remove((predecessor, node))
            for successor in self.graph.successors(node):
                if (node, successor) in self.added_edges:
                    self.added_edges.remove((node, successor))
                if (node, successor) not in self.removed_edges:
                    self.removed_edges.append((node, successor))
            self.graph.remove_node(node)
        return

    """def update_graph(self, new_graph):
        
        Takes a modification of the current graph and updates the lists added_edges and removed_edges
        :param new_graph: Modified version of the original graph
        
        old_edges = nx.get_edge_attributes(self.graph, 'weight').items()
        new_edges = nx.get_edge_attributes(new_graph, 'weight').items()
        for edge in list(set(new_edges) - set(old_edges)):
            self.add_edge(edge[0][0], edge[0][1], edge[1])"""

    def update_random_walks(self):
        """
        Takes the lists added_edges and removed_edges and recomputes all random walks that have traversed these
        edges, starting from their respective source nodes. The new random walks then replace the old ones in the
        list random_walks. Finally the edges are removed from the lists added_edges and removed_edges
        """
        for edge in reversed(self.added_edges):
            self.added_edges.remove(edge)
            random_walks_to_change = [random_walk for random_walk in self.random_walks if edge[0] in random_walk]
            for random_walk in random_walks_to_change:
                self.random_walks.remove(random_walk)
                del random_walk[random_walk.index(edge[0])+1:]
                self.add_random_walk(random_walk)

        for edge in reversed(self.removed_edges):
            self.removed_edges.remove(edge)
            random_walks_to_change = [random_walk for random_walk in self.random_walks if edge[0] in random_walk]
            for random_walk in random_walks_to_change:
                self.random_walks.remove(random_walk)
                del random_walk[random_walk.index(edge[0]) + 1:]
                self.add_random_walk(random_walk)
        return
