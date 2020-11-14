import random
from seed import merge
from graph import Cluster


def combine(clusterOne, clusterTwo):
    #self.nodes = []
    #self.edges = []
    #self.edge_cut = []
    #self.neighbors = []
    #if node != None:
    #    self.id = node.Id()
    #    self.pop = node.pop
    #    self.nodes.append(node)
    #else:
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


def rebalance(graph):
    clusterOne = random.choice(graph.Clusters())
    clusterTwo = random.choice(clusterOne.Neighbors())
