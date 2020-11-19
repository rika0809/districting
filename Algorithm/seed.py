import random


def merge(cluster, target, graph):
    cluster.nodes = cluster.nodes + target.nodes
    cluster.updatePop()
    cluster.updateEdges()

    for clu in target.neighbors:
        if cluster == clu:
            clu.removeNeighbor(target)
            continue
        if cluster not in clu.neighbors:
            clu.addNeighbor(cluster)
        if clu not in cluster.neighbors:
            cluster.addNeighbor(clu)
        clu.removeNeighbor(target)

    #for clu in graph.clusters:
    #    if target in clu.neighbors:
    #        clu.removeNeighbor(target)

    graph.removeCluster(target)


def generateSeed(graph):
    n = graph.numCluster # n districts

    for cluster in graph.clusters:
        cluster.updateEdges()

    while len(graph.clusters) != n:
        clusters = graph.clusters
        cluster = random.choice(clusters)
        target = random.choice(cluster.neighbors)
        merge(cluster, target, graph)




