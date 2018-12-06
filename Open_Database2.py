"""
The code below opens the multi-chain database and generates a graph of nodes corresponding to peers in the network
and edges representing the flow of data in between peers
"""
import sqlite3
import time

import networkx as nx
from Encode import decode


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
		print("graphreduction instantiated")

	def open_data_set(self):
		"""
		Accesses the trustchain data set and opens all rows. Then a graph is generated from all rows with nodes
		corresponding to public keys and edges corresponding to transactions.
		"""
		print("Trying to open database")
		conn = sqlite3.connect(self.file_path + self.file_name + ".db")
		print("succesfully opened")
		cursor = conn.cursor()
		print("Executing 'SELECT * FROM blocks' from query")
		cursor.execute("""SELECT * FROM blocks""")
		total_blocks = cursor.rowcount
		round_count = 0
		skipped_blocks = 0
		raw_block = cursor.fetchone()
		old_time = time.time() - 1  # Initialize to time a second ago to prevent division by zero at line 58

		# Dict where all the edges will be stored
		edges = {}
		while raw_block is not None:
			if (round_count % 5000) == 0:
				print("{} blocks parsed, {} bloccks skipped, at {} blocks/seconds".format(round_count, skipped_blocks,
																					5000 / (time.time() - old_time)))
				old_time = time.time()

			block = {"type": str(raw_block[0])}

			# For now we're only interested in bandwidth blocks,
			# se we don;t even need to decode any other block
			if block["type"] != 'tribler_bandwidth':
				raw_block = cursor.fetchone()
				skipped_blocks += 1
				round_count += 1
				continue

			# parse raw query data to python representation of the block
			block["tx"] = decode(str(raw_block[1]))[1]
			block["public key"] = str(raw_block[2]).encode('hex')  # Party A
			block["sequence number"] = raw_block[3]  # Sequence number
			block["counter public key"] = str(raw_block[4]).encode('hex')  # Party B
			block["link sequence number"] = raw_block[5]
			block["previous hash"] = str(raw_block[6]).encode('hex')
			block["block time_stamp"] = raw_block[8]
			block["insertion time"] = str(raw_block[9])
			block["hash"] = str(raw_block[10]).encode('hex')

			# If we convert all the edges in a universal direction they can be easier address
			# Here we sort alphabetically the sender-receiver pair, and flip the direction if needed
			# b -(5)-> a will be transferred to a -(-5)-> b. this makes it easy to detect double edges
			if block["public key"] > block["counter public key"]:
				# Swap sender receiver ID
				temp_key = block["public key"]
				block["public key"] = block["counter public key"]
				block["counter public key"] = temp_key

				size = block["tx"]["down"] - block["tx"]["up"]
			else:
				size = block["tx"]["up"] - block["tx"]["down"]

			try:
				new_size = edges[block["public key"]][block["counter public key"]] + size
				edges[block["public key"]][block["counter public key"]] = new_size
			except KeyError, e:
				try:
					edges[block["public key"]][block["counter public key"]] = size
				except KeyError, e:
					edges[block["public key"]] = {block["counter public key"]: size}

			raw_block = cursor.fetchone()
			round_count += 1

		current_node = 1
		total_nodes = len(edges)

		print("Extracted {} unique nodes from {} blocks".format(total_nodes, total_blocks))
		for party in edges:
			if (current_node % 100) == 0:
				print("{}/{} nodes added".format(current_node, total_nodes))

			for counterparty in edges[party]:
				size = edges[party][counterparty] / 2
				if size >= 0:
					self.graph.add_edge(party, counterparty, weight=size)
				else:
					self.graph.add_edge(counterparty, party, weight=-size)
			current_node += 1
		return

	def generate_graph(self):
		print("Generating graph")
		return self.graph
