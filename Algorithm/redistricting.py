import random
from seed import merge
from graph import Cluster, TreeNode
import networkx as nx
import matplotlib.pyplot as plt


def plot(graph):
    G = nx.Graph()
    fig, axes = plt.subplots(nrows=1, ncols=2)
    ax = axes.flatten()

    nodes = []
    colormap = []

    for node in graph.nodes:
        nodes.append(node.id)
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


def generate_tree(cluster):
    tree_nodes = []
    tree_edges = []

    s = random.choice(range(len(cluster.nodes)))

    for node in cluster.nodes:
        tree_nodes.append(TreeNode(node.id))

    visited = [False] * len(cluster.nodes)
    queue = []
    queue.append(cluster.nodes[s])
    visited[s] = True

    while len(queue) > 0:
        sourceNode = queue.pop(0)
        u_id = sourceNode.id
        #print("node" + str(u_id))
        for neighbor in sourceNode.neighbors:
            if neighbor in cluster.nodes:
                s = cluster.nodes.index(neighbor)
                if not visited[s]:
                    v_id = neighbor.id
                    tree_edges.append((u_id, v_id))
                    visited[s] = True
                    queue.append(cluster.nodes[s])

                    for treeNode in tree_nodes:
                        if treeNode.id == u_id:
                            treeNode.add_neighbor(v_id)
                        if treeNode.id == v_id:
                            treeNode.add_neighbor(u_id)

            else:
                continue
    return tree_nodes, tree_edges


def getClusterNodes(treeNodes, sourceNodeOne, sourceNodeTwo):
    nodesOne = []
    s = 0

    for i in range(len(treeNodes)):
        if treeNodes[i].id == sourceNodeOne.id:
            s = i
            break;

    visited = [False] * len(treeNodes)
    queue = []
    queue.append(sourceNodeOne)
    visited[s] = True

    while len(queue) > 0:
        sourceNode = queue.pop(0)
        nodesOne.append(sourceNode.id)
        for neighbor_id in sourceNode.neighbors:
            if neighbor_id != sourceNodeTwo.id:
                neighbor_node = None
                for i in range(len(treeNodes)):
                    if treeNodes[i].id == neighbor_id:
                        neighbor_node = treeNodes[i]
                        s = i
                        break
                if not visited[s]:
                    visited[s] = True
                    queue.append(neighbor_node)
            else:
                continue
    return nodesOne


def split(graph, edge, cluster):
    u_id, v_id = edge
    u = graph.find_node(u_id)
    v = graph.find_node(v_id)

    return


def rebalance(graph):
    clusterOne = random.choice(graph.clusters)
    clusterTwo = random.choice(clusterOne.neighbors)
    print("\n After rebalance: cluster[" + str(clusterOne.id)+"] and cluster[" + str(clusterTwo.id)+"]\n")
    print(len(graph.clusters))
    merge(clusterOne, clusterTwo, graph)

    treeNodes, treeEdges = generate_tree(clusterOne)
    

    # split two clusters
    while (1):
        cutEdge = random.choice(treeEdges)

        treeSourceNodeOne = None
        treeSourceNodeTwo = None
        oneId, twoId = cutEdge
        for treeNode in treeNodes:
            if treeNode.id == oneId:
                treeSourceNodeOne = treeNode
            if treeNode.id == twoId:
                treeSourceNodeTwo = treeNode
            if treeSourceNodeOne is not None and treeSourceNodeTwo is not None:
                break;

        nodesOne = getClusterNodes(treeNodes, treeSourceNodeOne, treeSourceNodeTwo)
        nodesTwo = getClusterNodes(treeNodes, treeSourceNodeTwo, treeSourceNodeOne)

        newclusterOne = Cluster()
        newclusterOne.id = treeSourceNodeOne.id
        for node in clusterOne.nodes:
            if node.id in nodesOne:
                newclusterOne.nodes.append(node)
        newclusterOne.update_edges()
        newclusterOne.update_pop()

        newclusterTwo = Cluster()
        newclusterTwo.id = treeSourceNodeTwo.id
        for node in clusterOne.nodes:
            if node.id in nodesTwo:
                newclusterTwo.nodes.append(node)
        newclusterTwo.update_edges()
        newclusterTwo.update_pop()
    ############################
    print("new clusters:" + str(newclusterOne.id) + ", "+ str(newclusterTwo.id))
    for node in newclusterOne.nodes:
        for neighborNode in node.neighbors:
            if neighborNode not in newclusterOne.nodes:
                neighborCluster = graph.find_cluster(neighborNode)
                if neighborCluster not in newclusterOne.neighbors and neighborCluster in clusterOne.neighbors:
                    newclusterOne.neighbors.append(neighborCluster)

    for node in newclusterTwo.nodes:
        for neighborNode in node.neighbors:
            if neighborNode not in newclusterTwo.nodes:
                neighborCluster = graph.find_cluster(neighborNode)
                if neighborCluster not in newclusterTwo.neighbors and neighborCluster in clusterOne.neighbors:
                    newclusterTwo.neighbors.append(neighborCluster)

    newclusterOne.neighbors.append(newclusterTwo)
    newclusterTwo.neighbors.append(newclusterOne)

    for clu in graph.clusters:
        if clusterOne in clu.neighbors:
            clu.remove_neighbor(clusterOne)

    graph.remove_cluster(clusterOne)

    for neighborCluster in clusterOne.neighbors:
        for u_id, v_id in neighborCluster.edge_cut:
            v = graph.find_node(v_id)
            if v in newclusterOne.nodes and newclusterOne not in neighborCluster.neighbors:
                neighborCluster.neighbors.append(newclusterOne)
            if v in newclusterTwo.nodes and newclusterTwo not in neighborCluster.neighbors:
                neighborCluster.neighbors.append(newclusterTwo)

    graph.clusters.append(newclusterOne)
    graph.clusters.append(newclusterTwo)

    print(len(graph.clusters))
    #graph.print_clusters()
    # plot(graph)
