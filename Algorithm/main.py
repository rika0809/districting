import json
import networkx as nx
import matplotlib.pyplot as plt

from redistricting import rebalance
from seed import generateSeed
from graph import Graph, Node

path = 'GA_precincts_simplified_plus (1).json'

if __name__ == '__main__':
    with open(path) as f:
        data = json.load(f)

    graph = Graph(14, 0.1, 100) # number of districts=14 ,1/2population variation: 0.9ideal~1.1ideal, edge-cut< 100

    for i in range(len(data['features'])):
        node = Node(data['features'][i]['properties']['ID'], data['features'][i]['properties']['TOTPOP'])
        graph.addNode(node)

    for i in range(len(data['features'])):
        id = data['features'][i]['properties']['ID']
        neighborsId = data['features'][i]['properties']['Neighbors']

        for neighborId in neighborsId:
            graph.addEdge(id, neighborId)

    graph.idealPop = int(graph.pop/graph.numCluster)

    generateSeed(graph)

    print("Ideal population: " + str(graph.idealPop))
    print("Population variation: " + str(2 * graph.populationVariation))
    print("Population valid range: " + str(graph.lowerBound) + "-" + str(graph.upperBound))
    print("Edge cut valid range: 0-" + str(graph.edgeCut))
    print('\n')

    ###################
    G1 = nx.Graph()
    G2 = nx.Graph()
    fig, axes = plt.subplots(nrows=1, ncols=2)
    ax = axes.flatten()

    nodes = []
    edges = []

    for cluster in graph.clusters:
        nodes.append(cluster.id)
    G1.add_nodes_from(nodes)

    for cluster in graph.clusters:
        u_id = cluster.id
        for neighbor_cluster in cluster.neighbors:
            v_id = neighbor_cluster.id
            if (u_id, v_id) not in edges and (v_id, u_id) not in edges:
                edges.append((u_id, v_id))

    G1.add_edges_from(edges)

    nx.draw(G1, with_labels=True, ax=ax[0])
    ax[0].set_axis_off()
    ###################





    graph.printClusters()

    print("\n\nRebalance...\n")
    print("--------------------------------------------------------------------------")
    rebalance(graph)












    ###################
    nodes = []
    edges = []

    for cluster in graph.clusters:
        nodes.append(cluster.id)
    G2.add_nodes_from(nodes)

    for cluster in graph.clusters:
        u_id = cluster.id
        for neighbor_cluster in cluster.neighbors:
            v_id = neighbor_cluster.id
            if (u_id, v_id) not in edges and (v_id, u_id) not in edges:
                edges.append((u_id, v_id))

    G2.add_edges_from(edges)

    nx.draw(G2, with_labels=True, ax=ax[1])
    ax[1].set_axis_off()

    plt.show()
