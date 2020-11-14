import random
from seed import merge
from graph import Cluster
import networkx as nx
import matplotlib.pyplot as plt


def plot(graph):
    G = nx.Graph()
    fig, axes = plt.subplots(nrows=1, ncols=2)
    ax = axes.flatten()

    nodes = []
    colormap = []

    for node in graph.nodes:
        nodes.append(node.Id())
    G.add_nodes_from(nodes)

    for node in G:
        if graph.find_node(node) in graph.clusters[0].nodes:
            colormap.append('red')
        if graph.find_node(node) in graph.clusters[1].nodes:
            colormap.append('blue')

    G.add_edges_from(graph.edges)
    nx.draw(G, with_labels=True, node_color=colormap, ax=ax[0])
    ax[0].set_axis_off()
    plt.show()
    return


def combine(clusterOne, clusterTwo):
    # self.nodes = []
    # self.edges = []
    # self.edge_cut = []
    # self.neighbors = []
    # if node != None:
    #    self.id = node.Id()
    #    self.pop = node.pop
    #    self.nodes.append(node)
    # else:
    #    self.id = 0
    #    self.pop = 0
    clusterOne.nodes = clusterOne.nodes + clusterTwo.nodes

    mergedCluster = Cluster()
    mergedCluster.nodes = clusterOne.nodes + clusterTwo.nodes
    mergedCluster.edges = clusterOne.edges + clusterTwo.edges
    for u_id, v_id in clusterOne.edge_cut:
        for node in clusterTwo.nodes:
            if node.id == u_id or node.id == v_id:
                mergedCluster.edges.append((u_id, v_id))
    return mergedCluster


def BFS(cluster):
    edges = []
    nodes = cluster.nodes
    s = random.choice(range(len(nodes)))
    node = nodes[s]

    visited = [False] * len(nodes)

    queue = []

    queue.append(node)

    visited[s] = True

    while len(queue) > 0:
        node = queue.pop(0)
        u_id = node.id
        for neighbor in node.neighbors:
            if neighbor in nodes:
                s = nodes.index(neighbor)
                if not visited[s]:
                    v_id = neighbor.id
                    edges.append((u_id, v_id))
                    visited[s] = True
                    queue.append(nodes[s])
            else:
                continue
    return edges


def generate_tree(cluster, graph):
    newEdges = BFS(cluster)
    oldEdges = cluster.edges
    nodes = cluster.nodes

    for u_id, v_id in oldEdges:
        u = graph.find_node(u_id)
        v = graph.find_node(v_id)

        u.neighbors.remove(v)
        v.neighbors.remove(u)
        if (u_id, v_id) in graph.edges:
            graph.edges.remove((u_id, v_id))
        else:
            graph.edges.remove((v_id, u_id))

    cluster.edges = newEdges

    for u_id, v_id in newEdges:
        u = graph.find_node(u_id)
        v = graph.find_node(v_id)

        u.neighbors.append(v)
        v.neighbors.append(u)
        graph.edges.append((u_id, v_id))


def rebalance(graph):
    clusterOne = random.choice(graph.Clusters())
    clusterTwo = random.choice(clusterOne.Neighbors())
    merge(clusterOne, clusterTwo, graph)
    generate_tree(clusterOne, graph)
    plot(graph)
