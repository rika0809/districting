import random


def merge(cluster, neighbor, graph):
    cluster.nodes = cluster.nodes + neighbor.nodes

    for clu in neighbor.neighbors:
        if cluster == clu:
            continue
        if cluster not in clu.neighbors:
            clu.neighbors.append(cluster)
        if clu not in cluster.neighbors:
            cluster.neighbors.append(clu)


    for clu in graph.clusters:
        if neighbor in clu.neighbors:
            clu.neighbors.remove(neighbor)

    graph.clusters.remove(neighbor)


def generate_seed(graph, n):  # need deal with len neighbors == 0
    while len(graph.clusters) != n:
        clusters = graph.clusters
        cluster = random.choice(clusters)
        neighbor = random.choice(cluster.neighbors)

        #graph.clusters.remove(neighbor_cluster)
        #cluster.combine(neighbor_cluster)
        merge(cluster, neighbor, graph)



