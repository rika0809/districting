import random
from graph import Graph
from seed import generateSeed
from redistricting import rebalance

graph = Graph(3, 0.2, 10)
graph.addNodeForms([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], [32,24,57,13,43, 34, 67, 35,58,54,27,48,90,46,23])
graph.addEdgeForms([(6, 7), (7, 8), (8, 5), (5, 6), (8, 9), (9, 10), (10, 5), (5, 4), (4, 3), (3, 11), (11, 10), (10, 12), (10, 15), (11, 12), (12, 15), (14, 15), (13, 14), (13, 1), (12, 13), (1, 2)])
graph.idealPop = 217

generateSeed(graph)
print("Ideal population: " + str(graph.idealPop))
print("Population variation: " + str(2*graph.populationVariation))
print("Population valid range: " + str(graph.lowerBound) + "-" + str(graph.upperBound))
print("Edge cut valid range: 0-"+ str(graph.edgeCut))
print('\n')
graph.printClusters()

print("\n\nRebalancing:...\n")
print("--------------------------------------------------------------------------")
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