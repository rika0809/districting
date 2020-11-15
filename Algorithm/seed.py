import random


def merge(cluster, target, graph):
    cluster.nodes = cluster.nodes + target.nodes
    cluster.update_pop()
    cluster.update_edges()

    for clu in target.neighbors:
        if cluster == clu:
            continue
        if cluster not in clu.neighbors:
            clu.add_neighbor(cluster)
        if clu not in cluster.neighbors:
            cluster.add_neighbor(clu)

    for clu in graph.clusters:
        if target in clu.neighbors:
            clu.remove_neighbor(target)

    graph.remove_cluster(target)


def generate_seed(graph):
    n = graph.numCluster
    for cluster in graph.clusters:
        cluster.update_edges()

    while len(graph.clusters) != n:
        clusters = graph.clusters
        cluster = random.choice(clusters)
        target = random.choice(cluster.neighbors)
        merge(cluster, target, graph)




