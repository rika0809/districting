import networkx as nx
from graph import *
from seed import *

MERGEDCLUSTERID = 9999


def generateTree(cluster):
    G = nx.Graph()
    G.add_edges_from(cluster.edges)

    spanningTree = nx.tree.minimum_spanning_edges(G, algorithm="kruskal", data=False)
    ST = nx.Graph()
    ST.add_edges_from(list(spanningTree))

    return ST


# create new cluster
def getNewCluster(graph, id, nodes, edges):
    newcluster = Cluster()

    newcluster.id = id
    for node in nodes:
        newcluster.nodes.append(graph.nodesDic[node])
        newcluster.pop += graph.nodesDic[node].pop
    newcluster.edges = edges

    return newcluster


def updateNeighbors(graph, mergedCluster, clusterOne, clusterTwo):
    for mergedClusterNode in mergedCluster.nodes:
        for neighborNode in mergedClusterNode.neighbors:
            if neighborNode not in clusterOne.nodes and neighborNode not in clusterTwo.nodes:  # it's an external node
                neighborCluster = graph.findCluster(neighborNode)  # find the external cluster the node belongs to

                # update clusterOne's neighbors and surrounded clusters's neighbors
                if mergedClusterNode in clusterOne.nodes:
                    if neighborCluster not in clusterOne.neighbors:
                        clusterOne.neighbors.append(neighborCluster)
                    if clusterOne not in neighborCluster.neighbors:
                        neighborCluster.neighbors.append(clusterOne)

                # update clusterTwo's neighbors and surrounded clusters's neighbors
                if mergedClusterNode in clusterTwo.nodes:
                    if neighborCluster not in clusterTwo.neighbors:
                        clusterTwo.neighbors.append(neighborCluster)
                    if clusterTwo not in neighborCluster.neighbors:
                        neighborCluster.neighbors.append(clusterTwo)

    # add each other as neighbor
    clusterOne.neighbors.append(clusterTwo)
    clusterTwo.neighbors.append(clusterOne)


def getNewClusters(graph, ST, cutEdge):
    oneID, twoID = cutEdge

    # find nodes on the edge to be cut
    nodesOne = list(ST.subgraph(c).copy() for c in nx.connected_components(ST))[0].nodes
    nodesTwo = list(set(ST.nodes) - set(nodesOne))

    # create new clusters
    newClusterOne = getNewCluster(graph, oneID, nodesOne, list(list(ST.subgraph(c).copy() for c in nx.connected_components(ST))[0].nodes))
    newClusterTwo = getNewCluster(graph, twoID, nodesTwo, list(list(ST.subgraph(c).copy() for c in nx.connected_components(ST))[0].nodes))

    return newClusterOne, newClusterTwo


def getCompactness(border, totalNodes):
    return totalNodes/border


def getPopAndComp(graph, nodes):
    pop = 0
    border = 0
    totalNodes = len(nodes)

    for nodeId in nodes:
        node = graph.nodesDic[nodeId]
        pop += node.pop
        for neighborNode in node.neighbors:
            if neighborNode.id not in nodes:
                border += 1
                break

    compact = getCompactness(border, totalNodes)

    return pop, compact


def findEdge(graph, ST, oldDifference, oldCompact):
    # use case 32. Calculate the acceptability of each newly generated sub-graph (required)
    treeEdges = list(ST.edges)
    notFind = True

    while (notFind):
        # randomly chose an edge to cut
        cutEdge = random.choice(treeEdges)
        treeEdges.remove(cutEdge)
        oneID, twoID = cutEdge
        ST.remove_edge(oneID, twoID)

        nodesOne = max(nx.connected_components(ST), key=len)
        nodesTwo = list(set(ST.nodes) - set(nodesOne))

        # calculate new population score
        popOne, compactOne = getPopAndComp(graph, nodesOne)
        popTwo, compactTwo = getPopAndComp(graph, nodesTwo)
        newDifference = abs(popOne - popTwo)
        newCompact = compactOne + compactTwo

        ST.add_edge(oneID, twoID)

        # use case 35. Repeat the steps above until you generate satisfy the termination condition (required)
        if isAcceptable(graph, popOne, compactOne) and isAcceptable(graph, popTwo, compactTwo):  # if acceptable
            return cutEdge
        if newDifference < oldDifference and newCompact > oldCompact:  # if improved
            return cutEdge
        if len(treeEdges)==0:
            return None


def split(graph, mergedCluster, cutEdge, ST):
    # cut the edge
    oneID, twoID = cutEdge
    ST.remove_edge(oneID, twoID)

    # generate new clusters
    newClusterOne, newClusterTwo = getNewClusters(graph, ST, cutEdge)

    # update new clusters' and surrounded cluster's neighbors
    updateNeighbors(graph, mergedCluster, newClusterOne, newClusterTwo)

    # erase the merged cluster from the graph
    for cluster in graph.clusters:
        if mergedCluster in cluster.neighbors:
            cluster.removeNeighbor(mergedCluster)
    graph.removeCluster(mergedCluster)

    # add new clusters on graph
    graph.clusters.append(newClusterOne)
    graph.clusters.append(newClusterTwo)


def merge(clusterOne, clusterTwo):
    # create an imaginary cluster
    mergedCluster = Cluster()

    #  update properties
    mergedCluster.nodes = clusterOne.nodes + clusterTwo.nodes
    mergedCluster.pop = clusterOne.pop + clusterTwo.pop
    mergedCluster.updateEdges()

    #  collect surrounded cluster as neighbors
    for neighborCluster in clusterOne.neighbors:
        if neighborCluster != clusterTwo and neighborCluster not in mergedCluster.neighbors:
            mergedCluster.neighbors.append(neighborCluster)

    for neighborCluster in clusterTwo.neighbors:
        if neighborCluster != clusterOne and neighborCluster not in mergedCluster.neighbors:
            mergedCluster.neighbors.append(neighborCluster)

    # give an id
    mergedCluster.id = MERGEDCLUSTERID

    return mergedCluster


def getCompact(cluster):
    border = 0

    for node in cluster.nodes:
        for neighborNode in node.neighbors:
            if neighborNode not in cluster.nodes:
                border += 1
                break

    compact = getCompactness(border, len(cluster.nodes))

    return compact


def isAcceptable(graph, pop, comp):
    upper = graph.upper
    lower = graph.lower
    if upper >= pop >= lower and comp > graph.compact:
        return True
    else:
        return False


def printDistricts(graph):
    outString = [["ID", "Population", "PopulationVariation", "Compactness"]]

    for cluster in graph.clusters:
        neighborsString = "["
        nodesString = "["

        for neighbor in cluster.neighbors:
            if neighbor != cluster.neighbors[-1]:
                neighborsString += str(neighbor.id) + ","
            else:
                neighborsString += str(neighbor.id) + "]"

        for node in cluster.nodes:
            if node != cluster.nodes[-1]:
                nodesString += str(node.id) + ","
            else:
                nodesString += str(node.id) + "]"

        outString.append([str(cluster.id), str(cluster.pop), str(abs(cluster.pop - graph.idealPop)), str(getCompact(cluster))])

    print('{:<8} {:<8}  {:<8}  {:<8}'.format(*outString[0]))

    for i in range(1, len(outString)):
        print('{:<8} {:<8}     {:<8}            {:<8}'.format(*outString[i]))
    print("--------------------------------------------------------------------------")


# Algorithm phase 2
def redistricting(graph, iterationLimit):
    n = 0

    while n < iterationLimit:  # use case 36. Terminate a single districting calculation (required)
        # use case 30. Generate a random districting satisfying constraints (required)
        clusterOne = random.choice(graph.clusters)
        clusterTwo = random.choice(clusterOne.neighbors)
        # old score
        oldVariation = abs(clusterOne.pop - clusterTwo.pop)
        oldCompact = getCompact(clusterOne) + getCompact(clusterTwo)

        # assume to merge the clusters, which means, the merged cluster is "imaginary"
        mergedCluster = merge(clusterOne, clusterTwo)

        # use case 31. Generate a spanning tree of the combined sub-graph above (required)
        ST = generateTree(mergedCluster)

        # use case 33. Generate a feasible set of edges in the spanning tree to cut (required)
        cutEdge = findEdge(graph, ST, oldVariation, oldCompact)

        if cutEdge == None:
            continue
        else:
            # merge the clusters in real
            combine(clusterOne, clusterTwo, graph)

            # use case 34. Cut the edge in the combined sub-graph (required)
            split(graph, clusterOne, cutEdge, ST)

            printDistricts(graph)

            n += 1