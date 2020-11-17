import json

import networkx as nx
import matplotlib.pyplot as plt

from seed import generate_seed
from graph import Graph, Node
from redistricting import rebalance





if __name__ == '__main__':
    with open('GA_precincts_simplified_plus (1).json') as f:
        data = json.load(f)

    graph = Graph(14, 0.1, 100)

    for i in range(len(data['features'])):
        node = Node(data['features'][i]['properties']['ID'], data['features'][i]['properties']['TOTPOP'])
        graph.add_node(node)

    for i in range(len(data['features'])):
        id = data['features'][i]['properties']['ID']
        neighbors_id = data['features'][i]['properties']['Neighbors']

        for neighbor_id in neighbors_id:
            graph.add_edge(id, neighbor_id)

    generate_seed(graph)

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

    graph.print_clusters()
    print("\n\n After iteration:")
    rebalance(graph)

    graph.print_clusters()

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
