# Import Alexander Stannat's db->graph library
from Open_Database2 import GraphReduction2
import networkx as nx

file_path = 'D:\\4 - GitRepos\Incremental-Pagerank'
file_name = "\\trustchain"

gr = GraphReduction2(file_path, file_name)
gr.open_data_set()
graph = gr.generate_graph()

print("Storing pickled version")
nx.write_gpickle(graph, "./Results/MegaGraph.gpickle")
print("Reading the pickle file")
graph = nx.read_gpickle("./Results/MegaGraph.gpickle")

print("Generating degree list")
degree_list = graph.degree()

string_degree = str(degree_list)
print("Storing degrees to disk")
text_file = open("./Results/result.txt", "w")
# some dirty inline replacements, to make it directly importable in excel
text_file.write(string_degree.replace("),", "\n"))
text_file.close()
