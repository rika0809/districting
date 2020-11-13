import networkx as nx
import matplotlib.pyplot as plt
from graph import Graph
from seed import generate_seed


graph = Graph()
graph.add_node_forms([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], [321,2456,567,132,943, 324, 647, 3765,958,354,627,948,904, 546,323])
graph.add_edge_forms([(6, 7), (7, 8), (8, 5), (5, 6), (8, 9), (9, 10), (10, 5), (5, 4), (4, 3), (3, 11), (11, 10), (10, 12), (10, 15), (11, 12), (12, 15), (14, 15), (13, 14), (13, 1), (12, 13), (1, 2)])

generate_seed(graph, 3)
graph.print_clusters()

G = nx.Graph()
nodes = []
for node in graph.Nodes():
    nodes.append(node.Id())
G.add_nodes_from(nodes)
G.add_edges_from(graph.edges)
nx.draw(G, with_labels=True)
plt.savefig("path_graph1.png")
plt.show()