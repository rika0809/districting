import random


def generate_seed(graph, n):  # need deal with len neighbors == 0
    while len(graph.clusters) != n:
        clusters = graph.clusters
        cluster = random.choice(clusters)
        # print("Cluster has:")
        # print(cluster.nodes)
        neighbor_cluster = random.choice(cluster.neighbors)
        # print("Neighbor has:")
        # print(neighbor_cluster .nodes)
        graph.clusters.remove(neighbor_cluster)
        cluster.combine(neighbor_cluster)
        # print("After merging current cluster has:")
        # print(cluster.nodes)
        # print("-------------------")
        # for cluster in cluster.neighbors[0].neighbors:
        #    cluster.print_cluster()
