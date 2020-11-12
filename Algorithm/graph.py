class Vertex:
    def __init__(self, id):
        self.id = id
        self.neighbors_id = []

    def add_neighbor(self, neighbor_id):
        if neighbor_id not in self.neighbors_id:
            self.neighbors_id.append(neighbor_id)


class Cluster:
    def __init__(self, vertex_id):
        self.nodes = []
        self.nodes.append(vertex_id)
        self.neighbors = []

    def print_cluster(self):
        s = "["
        for node in self.nodes:
            if node != self.nodes[-1]:
                s += str(node) + ","
            else:
                s += str(node) + "]"
        print(s)


class Graph:
    def __init__(self):
        self.vertices = {}
        self.clusters = []

    def find_cluster(self, v_id):
        for cluster in self.clusters:
            if v_id in cluster.nodes:
                return cluster
        return None

    def find_vertex(self, v_id):
        return self.vertices[v_id]

    def add_vertex(self, vertex):
        if vertex.id not in self.vertices.keys():
            self.vertices[vertex.id] = vertex
            self.clusters.append(Cluster(vertex.id))
            return True
        else:
            return False

    def add_edge(self, u_id, v_id):
        if u_id in self.vertices.keys() and v_id in self.vertices.keys():
            self.vertices[u_id].add_neighbor(v_id)
            self.vertices[v_id].add_neighbor(u_id)
            u_cluster = self.find_cluster(u_id)
            v_cluster = self.find_cluster(v_id)
            if v_cluster not in u_cluster.neighbors:
                u_cluster.neighbors.append(v_cluster)
            if u_cluster not in v_cluster.neighbors:
                v_cluster.neighbors.append(u_cluster)
            return True
        else:
            return False

    def print_graph(self):
        for id in self.vertices.keys():
            s = str(id) + ': '
            print(s)
            print(self.vertices[id].neighbors_id)

    def print_clusters(self):
        for cluster in self.clusters:
            cluster.print_cluster()
