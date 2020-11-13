import random


def merge(cluster, neighbor, graph):
    cluster.setNodes(cluster.Nodes() + neighbor.Nodes())
    cluster.update_pop()

    for clu in neighbor.Neighbors():
        if cluster == clu:
            continue
        if cluster not in clu.Neighbors():
            clu.add_neighbor(cluster)
        if clu not in cluster.Neighbors():
            cluster.add_neighbor(clu)

    for clu in graph.Clusters():
        if neighbor in clu.Neighbors():
            clu.remove_neighbor(neighbor)

    graph.remove_cluster(neighbor)


def generate_seed(graph, n):
    while len(graph.clusters) != n:
        clusters = graph.Clusters()
        cluster = random.choice(clusters)
        neighbor = random.choice(cluster.Neighbors())

        #graph.clusters.remove(neighbor_cluster)
        #cluster.combine(neighbor_cluster)
        merge(cluster, neighbor, graph)



