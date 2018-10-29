"""
The code below performs a set of tests on the Incremental Personalized PageRank class
"""
import unittest
import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy
from Page_Rank2 import IncrementalPersonalizedPageRank2
from Page_Rank import IncrementalPersonalizedPageRank

class Tests(unittest.TestCase):

    def test_page_rank_1(self):
        """
        Test a very simple page rank computation without updating the graph
        """
        self.graph = nx.DiGraph()
        self.nodes = ['a', 'b', 'c']
        self.edges = [('a', 'b', 1), ('a', 'c', 2)]

        self.graph.add_nodes_from(self.nodes)
        self.graph.add_weighted_edges_from(self.edges)

        # pr = IncrementalPersonalizedPageRank(self.graph, 'a', 200, 0.05, 100)

        pr = IncrementalPersonalizedPageRank2(self.graph, 'a', 300, 0.05)
        pr.initial_random_walks()
        page_ranks = pr.compute_personalized_page_ranks()
        page_ranks_2 = nx.pagerank(self.graph, alpha=0.95, personalization={'a': 1, 'b': 0, 'c': 0},
                                   max_iter=500, weight='weight')
        self.assertTrue('a' in page_ranks)
        self.assertTrue('b' in page_ranks)
        self.assertTrue('c' in page_ranks)
        self.assertEqual(len(pr.random_walks), 300)

        # for walk in pr.random_walks:
        #   self.assertEqual(len(walk), 100)

        self.assertFalse(pr.removed_edges)
        self.assertFalse(pr.added_edges)
        self.assertGreaterEqual(page_ranks['a'], page_ranks['b'])
        self.assertGreaterEqual(page_ranks['a'], page_ranks['c'])

        for node in self.graph.nodes():
            self.assertAlmostEqual(page_ranks[node], page_ranks_2[node], 1)

    def test_page_rank_2(self):
        """
        Test page rank and update the graph
        """
        self.graph = nx.DiGraph()
        self.nodes = ['a', 'b', 'c']
        self.edges = [('a', 'b', 1), ('a', 'c', 2)]

        self.graph.add_nodes_from(self.nodes)
        self.graph.add_weighted_edges_from(self.edges)

        # pr = IncrementalPersonalizedPageRank(self.graph, 'a', 200, 0.05, 100)

        pr = IncrementalPersonalizedPageRank2(self.graph, 'a', 200, 0.05)
        pr.initial_random_walks()
        page_ranks = pr.compute_personalized_page_ranks()
        page_ranks_2 = nx.pagerank(self.graph, alpha=0.95, personalization={'a': 1, 'b': 0, 'c': 0},
                                   max_iter=500, weight='weight')
        for node in pr.graph.nodes():
            self.assertAlmostEqual(page_ranks[node], page_ranks_2[node], 1)

        pr.add_node('d')
        pr.add_edge('c', 'd', 2)
        pr.remove_edge('a', 'b')
        pr.remove_node('b')
        pr.add_weight_to_edge('a', 'c', -5)

        self.assertTrue('d' in pr.graph.nodes)
        self.assertTrue(('c', 'd', 2) in pr.added_edges)
        self.assertTrue(('c', 'd') in pr.graph.edges)
        self.assertFalse('b' in pr.graph.nodes)
        self.assertFalse(('a', 'b') in pr.graph.edges)
        self.assertTrue(('a', 'b') in pr.removed_edges)
        self.assertTrue(('c', 'a') in pr.graph.edges)
        self.assertFalse(('a', 'c') in pr.graph.edges)
        for edge in pr.graph.edges:
            self.assertTrue(pr.graph[edge[0]][edge[1]]['weight'] > 0)

        pr.update_random_walks()
        new_page_ranks = pr.compute_personalized_page_ranks()
        new_page_ranks_2 = nx.pagerank(pr.graph, alpha=0.95, personalization={'a': 1},
                                       max_iter=500, weight='weight')
        self.assertFalse(pr.removed_edges)
        self.assertFalse(pr.added_edges)
        self.assertFalse('b' in new_page_ranks)
        self.assertEqual(new_page_ranks['a'], 1)
        self.assertEqual(new_page_ranks['c'], 0)
        self.assertEqual(new_page_ranks['d'], 0)
        self.assertEqual(len(pr.random_walks), 200)

        # for walk in pr.random_walks:
        #   self.assertEqual(len(walk), 100)

        for node in self.graph.nodes:
            self.assertAlmostEqual(new_page_ranks[node], new_page_ranks_2[node], 2)

    def test_page_rank_3(self):
        """
        We test a personalized page rank on an empty graph
        """
        self.graph = nx.DiGraph()

        # pr = IncrementalPersonalizedPageRank(self.graph, None, 200, 0.05, 50)

        pr = IncrementalPersonalizedPageRank2(self.graph, None, 200, 0.05)
        page_ranks = pr.compute_personalized_page_ranks()
        self.assertEqual(page_ranks, {})

    def test_page_rank_4(self):
        """
        We test the page rank algorithm on a more intricate graph
        """
        self.graph = nx.DiGraph()
        self.nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        self.edges = [('a', 'c', 3), ('c', 'b', 4), ('b', 'e', 2), ('e', 'f', 1), ('c', 'd', 4), ('d', 'a', 2)]
        self.graph.add_nodes_from(self.nodes)
        self.graph.add_weighted_edges_from(self.edges)

        # pr = IncrementalPersonalizedPageRank(self.graph, 'a', 200, 0.05, 50)

        pr = IncrementalPersonalizedPageRank2(self.graph, 'a', 200, 0.05)
        pr.initial_random_walks()
        page_ranks = pr.compute_personalized_page_ranks()
        page_ranks_2 = nx.pagerank(pr.graph, alpha=0.95, personalization={'a': 1, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0},
                                   max_iter=500, weight='weight')

        for node in pr.graph.nodes():
            self.assertAlmostEqual(page_ranks[node], page_ranks_2[node], 1)

        pr.add_weight_to_edge('c', 'a', 3)
        pr.remove_node('f')
        pr.add_edge('d', 'g', 10)
        pr.add_weight_to_edge('a', 'd', 3)
        pr.add_weight_to_edge('e', 'b', 3)
        pr.update_random_walks()

        new_page_ranks = pr.compute_personalized_page_ranks()
        new_page_ranks_2 = nx.pagerank(pr.graph, alpha=0.95, personalization={'a': 1, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'g': 0},
                                       max_iter=500, weight='weight')
        for node in pr.graph.nodes:
            self.assertAlmostEqual(new_page_ranks[node], new_page_ranks_2[node], 1)

        self.assertFalse(pr.graph.has_edge('a', 'c'))
        self.assertFalse(pr.graph.has_edge('c', 'a'))
        self.assertFalse('f' in new_page_ranks.keys())

        # for random_walk in pr.random_walks:
        #    self.assertEqual(set(random_walk), {'a', 'd', 'g'})

        pr.add_edge('a', 'c', 3)
        pr.add_node('f')
        pr.add_edge('f', 'e', -1)
        pr.remove_edge('d', 'g')
        pr.add_weight_to_edge('e', 'b', -3)
        pr.add_weight_to_edge('d', 'a', 3)

        pr.update_random_walks()
        new_old_page_ranks = pr.compute_personalized_page_ranks()
        new_old_page_ranks_2 = nx.pagerank(pr.graph, alpha=0.95, personalization={'a': 1},
                                           max_iter=500, weight='weight')

        for node in pr.graph.nodes:
            self.assertAlmostEqual(new_old_page_ranks[node], new_old_page_ranks_2[node], 1)
        self.assertEqual(pr.graph.nodes, self.graph.nodes)
        self.assertEqual(pr.graph.edges, self.graph.edges)
        self.assertEqual(page_ranks.keys(), new_old_page_ranks.keys())
        for node in pr.graph.nodes:
            self.assertAlmostEqual(page_ranks[node], new_old_page_ranks[node], 1)
        self.assertFalse(pr.removed_edges)
        self.assertFalse(pr.added_edges)

    def test_page_rank_5(self):
        self.graph = nx.DiGraph()
        self.number_of_nodes = random.randint(2, 10000)
        self.nodes = range(self.number_of_nodes)
        personalization_list = [0 for _ in range(len(self.nodes))]
        personalization_list[0] = 1
        personalization_dict = dict(zip(self.nodes, personalization_list))
        self.graph.add_nodes_from(self.nodes)
        for _ in range(2*self.number_of_nodes):
            node_1 = random.choice(list(self.graph.nodes()))
            node_2 = random.choice(list(set(self.graph.nodes()) - {node_1}))
            if self.graph.has_edge(node_1, node_2) or self.graph.has_edge(node_2, node_1):
                continue
            else:
                weight = random.randint(1, 10)
                self.graph.add_weighted_edges_from([(node_1, node_2, weight)])

        pr = IncrementalPersonalizedPageRank2(self.graph, 0, 500, 0.3)
        pr.initial_random_walks()
        page_ranks = pr.compute_personalized_page_ranks()
        page_ranks_2 = nx.pagerank(pr.graph, alpha=0.7, personalization=personalization_dict,
                                   max_iter=500, weight='weight')

        # nx.draw_circular(pr.graph, with_labels=True, node_size=20, with_edge_labels=True)
        # plt.show()
        print self.number_of_nodes
        diff = numpy.linalg.norm(numpy.array(page_ranks.values()) - numpy.array(page_ranks_2.values())) / \
            numpy.linalg.norm(numpy.array(page_ranks_2.values()))
        self.assertAlmostEqual(diff, 0, 1)

        # pr = IncrementalPersonalizedPageRank(self.graph, 0, 200, 0.05, 50)
        pr = IncrementalPersonalizedPageRank2(self.graph, 0, 200, 0.05)
        pr.initial_random_walks()
        page_ranks = pr.compute_personalized_page_ranks()
        page_ranks_2 = nx.pagerank(pr.graph, alpha=0.95, personalization={0: 1},
                                   max_iter=500, weight='weight')
        # nx.draw_circular(pr.graph, with_labels=True, node_size=20, with_edge_labels=True)
        # plt.show()
        print "Random Walks: ", pr.random_walks

        print "Initial Page Ranks: ", "\n", page_ranks, "\n", page_ranks_2
        # print numpy.linalg.norm(numpy.array(page_ranks.values()) - numpy.array(page_ranks_2.values()))
        for node in pr.graph.nodes:
            self.assertAlmostEqual(page_ranks[node], page_ranks_2[node], 1)

        c = random.randint(self.number_of_nodes//4, self.number_of_nodes//2)
        choices = ["Remove Edge / Add Edge", "Change Edge Weight", "Remove Node / Add Node"]
        for _ in range(c):
            choice = random.choice(choices)
            if choice == "Remove Edge / Add Edge":
                node_1 = random.choice(list(pr.graph.nodes))
                node_2 = random.choice(list(set(pr.graph.nodes) - {node_1}))
                if pr.graph.has_edge(node_1, node_2):
                    pr.remove_edge(node_1, node_2)
                elif pr.graph.has_edge(node_2, node_1):
                    pr.remove_edge(node_2, node_1)
                else:
                    weight = random.randint(-10, 10)
                    pr.add_edge(node_1, node_2, weight)
            elif choice == "Change Edge Weight":
                edge = random.choice(list(pr.graph.edges))
                weight = random.randint(-10, 10)
                pr.add_weight_to_edge(edge[0], edge[1], weight)
            elif choice == "Remove Node / Add Node":
                w = random.randint(0, 1)
                if w == 0:
                    pr.add_node(self.number_of_nodes + 1)
                    self.number_of_nodes += 1
                elif w == 1:
                    node = random.choice(list(set(pr.graph.nodes) - {0}))
                    pr.remove_node(node)

        # nx.draw_circular(self.graph, with_labels=True, node_size=20, with_edge_labels=True)
        # plt.show()

        pr.update_random_walks()
        new_page_ranks = pr.compute_personalized_page_ranks()
        new_page_ranks_2 = nx.pagerank(pr.graph, alpha=0.7, personalization={0: 1},
                                       max_iter=1000, weight='weight')
        print self.number_of_nodes
        diff = numpy.linalg.norm(numpy.array(new_page_ranks.values()) - numpy.array(new_page_ranks_2.values())) / \
            numpy.linalg.norm(numpy.array(new_page_ranks_2.values()))
        self.assertAlmostEqual(diff, 0, delta=0.06)

        # nx.draw_circular(self.graph, with_labels=True, node_size=20, with_edge_labels=True)
        # plt.show()


if __name__ == '__main__':
    unittest.main()

