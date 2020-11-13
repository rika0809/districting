class Node:
    def __init__(self, id, pop):
        self.id = id
        self.neighbors = []
        self.pop = pop

    def add_neighbor(self, neighbor_node):
        if neighbor_node not in self.neighbors:
            self.neighbors.append(neighbor_node)

    def Id(self):
        return self.id

    def Pop(self):
        return self.pop


class Cluster:
    def __init__(self, node):
        self.id = node.Id()
        self.nodes = []
        self.nodes.append(node)
        self.neighbors = []
        self.pop = node.pop

    def Nodes(self):
        return self.nodes

    def Neighbors(self):
        return self.neighbors

    def add_neighbor(self, cluster):
        self.neighbors.append(cluster)

    def remove_neighbor(self, cluster):
        self.neighbors.remove(cluster)

    def setNodes(self, nodes):
        self.nodes = nodes

    def update_pop(self):
        self.pop = 0
        for node in self.nodes:
            self.pop += node.pop

    def print_cluster(self):
        s = "ID: " + str(self.id) + ", Population: " + str(self.pop) + ", Neighbors:["

        for cluster in self.neighbors:
            if cluster != self.neighbors[-1]:
                s += str(cluster.id) + ","
            else:
                s += str(cluster.id) + "], \nPrecincts:["

        for node in self.nodes:
            if node != self.nodes[-1]:
                s += str(node.Id()) + ","
            else:
                s += str(node.Id()) + "]"

        print(s)
        print("-------------------------------------------")


class Graph:
    def __init__(self):
        self.nodes = []
        self.clusters = []
        self.edges = []
        self.pop = 0

    def find_cluster(self, node):
        for cluster in self.clusters:
            if node in cluster.Nodes():
                return cluster
        return None

    def find_node(self, n_id):
        for node in self.nodes:
            if node.Id() == n_id:
                return node
        return None

    def add_node(self, node):
        self.nodes.append(node)
        self.clusters.append(Cluster(node))
        self.pop += node.Pop()

    def add_edge(self, u_id, v_id):
        u = self.find_node(u_id)
        v = self.find_node(v_id)
        u.add_neighbor(v)
        v.add_neighbor(u)
        self.edges.append((u_id, v_id))
        u_cluster = self.find_cluster(u)
        v_cluster = self.find_cluster(v)
        if v_cluster not in u_cluster.Neighbors():
            u_cluster.add_neighbor(v_cluster)
        if u_cluster not in v_cluster.Neighbors():
            v_cluster.add_neighbor(u_cluster)

    def add_node_forms(self, node_forms, pop_forms):
        for i in range(len(node_forms)):
            node = Node(node_forms[i], pop_forms[i])
            self.add_node(node)

    def add_edge_forms(self, edge_forms):
        for u_id, v_id in edge_forms:
            self.add_edge(u_id, v_id)

    def print_clusters(self):
        for cluster in self.clusters:
            cluster.print_cluster()

    def totPop(self):
        return self.pop

    def Clusters(self):
        return self.clusters

    def remove_cluster(self, cluster):
        self.clusters.remove(cluster)