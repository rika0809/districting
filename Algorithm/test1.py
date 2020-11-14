for cluster in graph.clusters:
    if len(cluster.nodes) == 1:
        node = cluster.nodes[0]
        for neighbor_node in node.neighbors:
            cluster.edge_cut.append((node.id, neighbor_node.id))