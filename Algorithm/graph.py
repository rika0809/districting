class TreeNode:
    def __init__(self, id):
        self.id = id
        self.neighbors = []

    def add_neighbor(self, neighbor_id):
        if neighbor_id not in self.neighbors:
            self.neighbors.append(neighbor_id)


class Node:
    def __init__(self, id, pop=None):
        self.id = id
        self.neighbors = []
        if pop != None:
            self.pop = pop

    def add_neighbor(self, neighbor_node):
        if neighbor_node not in self.neighbors:
            self.neighbors.append(neighbor_node)


class Cluster:
    def __init__(self, node=None):
        self.nodes = []
        self.edges = []
        self.edge_cut = []
        self.neighbors = []
        if node != None:
            self.id = node.id
            self.pop = node.pop
            self.nodes.append(node)
        else:
            self.id = 0
            self.pop = 0

    def add_neighbor(self, cluster):
        self.neighbors.append(cluster)

    def remove_neighbor(self, cluster):
        self.neighbors.remove(cluster)

    def update_pop(self):
        self.pop = 0
        for node in self.nodes:
            self.pop += node.pop

    def update_edges(self):
        self.edges = []
        self.edge_cut = []
        for node in self.nodes:
            u_id = node.id
            for neighbor in node.neighbors:
                v_id = neighbor.id
                if neighbor in self.nodes:
                    if ((u_id, v_id) not in self.edges) and ((v_id, u_id) not in self.edges):
                        self.edges.append((u_id, v_id))
                else:
                    if ((u_id, v_id) not in self.edge_cut) and ((v_id, u_id) not in self.edge_cut):
                        self.edge_cut.append((u_id, v_id))

    def print_cluster(self):
        s = "ID: " + str(self.id) + ", Population: " + str(self.pop) + ", Edge-cut: " + str(
            len(self.edge_cut)) + ", Neighbors:["

        for cluster in self.neighbors:
            if cluster != self.neighbors[-1]:
                s += str(cluster.id) + ","
            else:
                s += str(cluster.id) + "], \nPrecincts:["

        for node in self.nodes:
            if node != self.nodes[-1]:
                s += str(node.id) + ","
            else:
                s += str(node.id) + "]"

        print(s)
        print("-------------------------------------------")


class Graph:
    def __init__(self, numCluster, populationVariation):
        self.nodes = []
        self.clusters = []
        self.edges = []
        self.pop = 0
        self.numCluster = numCluster
        self.populationVariation = populationVariation
        self.lowerBound = 0
        self.upperBound = 0

    def find_cluster(self, node):
        for cluster in self.clusters:
            if node in cluster.nodes:
                return cluster
        return None

    def find_node(self, n_id):
        for node in self.nodes:
            if node.id == n_id:
                return node
        return None

    def add_node(self, node):
        self.nodes.append(node)
        self.clusters.append(Cluster(node))
        self.pop += node.pop
        self.updateBounds()

    def add_edge(self, u_id, v_id):
        u = self.find_node(u_id)
        v = self.find_node(v_id)
        if u not in v.neighbors and v not in u.neighbors:
            u.add_neighbor(v)
            v.add_neighbor(u)
            self.edges.append((u_id, v_id))
            u_cluster = self.find_cluster(u)
            v_cluster = self.find_cluster(v)
            if v_cluster not in u_cluster.neighbors:
                u_cluster.add_neighbor(v_cluster)
            if u_cluster not in v_cluster.neighbors:
                v_cluster.add_neighbor(u_cluster)

    def add_node_forms(self, node_forms, pop_forms):
        for i in range(len(node_forms)):
            node = Node(node_forms[i], pop_forms[i])
            self.add_node(node)

    def add_edge_forms(self, edge_forms):
        for u_id, v_id in edge_forms:
            self.add_edge(u_id, v_id)

    def print_clusters(self):
        print("Population valid range:" + str(int(self.lowerBound)) + "-" + str(int(self.upperBound)))
        for cluster in self.clusters:
            cluster.print_cluster()

    def totPop(self):
        return self.pop

    def idealPop(self):
        return self.pop / len(self.clusters)

    def remove_cluster(self, cluster):
        self.clusters.remove(cluster)

    def updateBounds(self):
        ideal = self.pop/self.numCluster
        self.lowerBound = ideal - ideal * self.populationVariation
        self.upperBound = ideal + ideal * self.populationVariation
