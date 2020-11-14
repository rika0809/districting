import random
from graph import Graph
from seed import generate_seed
from redistricting import rebalance

graph = Graph()
graph.add_node_forms([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], [32,24,57,13,43, 34, 67, 35,58,54,27,48,90,46,23])
graph.add_edge_forms([(6, 7), (7, 8), (8, 5), (5, 6), (8, 9), (9, 10), (10, 5), (5, 4), (4, 3), (3, 11), (11, 10), (10, 12), (10, 15), (11, 12), (12, 15), (14, 15), (13, 14), (13, 1), (12, 13), (1, 2)])

generate_seed(graph, 3)
graph.print_clusters()
print("after merging:")

rebalance(graph)












#BFS(graph.clusters[0])
#print()

#print(graph.clusters[0].id)
#print(graph.clusters[0].edges)
#print(graph.clusters[0].edge_cut)
#print(graph.clusters[1].id)
#print(graph.clusters[1].edges)
#print(graph.clusters[1].edge_cut)
#print(graph.clusters[2].id)
#print(graph.clusters[2].edges)
#print(graph.clusters[2].edge_cut)

#c = rebalance(graph)
#G = nx.Graph()
#nodes = []
#edges = BFS(c)
#for node in c.nodes:
#    nodes.append(node.Id())
#G.add_nodes_from(nodes)
#G.add_edges_from(edges)
#nx.draw(G, with_labels=True)
#plt.savefig("path_graph1.png")
#plt.show()