import random
import threading
from graph import Cluster, TreeNode
from seed import combine

MERGEDCLUSTERID = 9999
threadLock = threading.Lock()


# BFS to generate a spinning tree
def generateTree(cluster):
    treeNodes = []
    treeEdges = []

    s = random.choice(range(len(cluster.nodes)))  # randomly select a node as start point

    for node in cluster.nodes:  # collect tree nodes
        treeNodes.append(TreeNode(node.id))

    visited = [False] * len(cluster.nodes)
    queue = []
    queue.append(cluster.nodes[s])
    visited[s] = True

    while len(queue) > 0:
        sourceNode = queue.pop(0)
        uid = sourceNode.id

        for neighbor in sourceNode.neighbors:
            if neighbor in cluster.nodes:
                s = cluster.nodes.index(neighbor)
                if not visited[s]:

                    # add treeEdge
                    vid = neighbor.id
                    treeEdges.append((uid, vid))
                    for treeNode in treeNodes:
                        if treeNode.id == uid:
                            treeNode.addNeighbor(vid)
                        if treeNode.id == vid:
                            treeNode.addNeighbor(uid)

                    visited[s] = True
                    queue.append(cluster.nodes[s])
            else:
                continue

    return treeNodes, treeEdges


# BFS to traverse a cluster and get node
def getClusterNodes(treeNodes, sourceNodeOne, sourceNodeTwo):
    nodesOne = []
    s = 0

    for i in range(len(treeNodes)):
        if treeNodes[i].id == sourceNodeOne.id:
            s = i
            break;

    visited = [False] * len(treeNodes)
    queue = []
    queue.append(sourceNodeOne)
    visited[s] = True

    while len(queue) > 0:
        sourceNode = queue.pop(0)
        nodesOne.append(sourceNode.id)
        for neighborId in sourceNode.neighbors:
            if neighborId != sourceNodeTwo.id:  # don't enter the node on the other cluster

                # get the neighborNode
                neighborNode = None
                for i in range(len(treeNodes)):
                    if treeNodes[i].id == neighborId:
                        neighborNode = treeNodes[i]
                        s = i
                        break

                if not visited[s]:
                    visited[s] = True
                    queue.append(neighborNode)
            else:
                continue

    return nodesOne


# if a single cluster is acceptable?
def isAcceptable(graph, cluster):
    upper = graph.upperBound
    lower = graph.lowerBound
    if upper >= cluster.pop >= lower:
        return True
    else:
        return False


# if all clusters on the graph acceptable?
def isAllAcceptable(graph):
    for cluster in graph.clusters:
        if not isAcceptable(graph, cluster):
            return False
    return True


# create new cluster
def getNewCluster(id, nodes, mergedCluster):
    newcluster = Cluster()

    newcluster.id = id
    for node in mergedCluster.nodes:
        if node.id in nodes:
            newcluster.nodes.append(node)
    newcluster.updateEdges()
    newcluster.updatePop()

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


# for example, parameter: edge(1,2), return node(1), node(2)
def findNodesOnCutEdge(treeNodes, cutEdge):
    treeSourceNodeOne = None
    treeSourceNodeTwo = None
    oneId, twoId = cutEdge

    # find the nodes from the tree nodes set
    for treeNode in treeNodes:
        if treeNode.id == oneId:
            treeSourceNodeOne = treeNode
        if treeNode.id == twoId:
            treeSourceNodeTwo = treeNode
        if treeSourceNodeOne is not None and treeSourceNodeTwo is not None:
            break;

    return treeSourceNodeOne, treeSourceNodeTwo


def getNewClusters(treeNodes, cutEdge, mergedCluster):
    # find nodes on the edge to be cut
    treeSourceNodeOne, treeSourceNodeTwo = findNodesOnCutEdge(treeNodes, cutEdge)

    nodesOne = getClusterNodes(treeNodes, treeSourceNodeOne, treeSourceNodeTwo)
    nodesTwo = getClusterNodes(treeNodes, treeSourceNodeTwo, treeSourceNodeOne)

    # create new clusters
    newClusterOne = getNewCluster(treeSourceNodeOne.id, nodesOne, mergedCluster)
    newClusterTwo = getNewCluster(treeSourceNodeTwo.id, nodesTwo, mergedCluster)

    return newClusterOne, newClusterTwo


def getFeasibleEdges(graph, newScores, edges, treeNodes, cutEdge, mergedCluster, oldDifference):
    # generate new clusters
    newClusterOne, newClusterTwo = getNewClusters(treeNodes, cutEdge, mergedCluster)

    # calculate new score
    newDifference = abs(newClusterOne.pop - newClusterTwo.pop)

    # use case 35. Repeat the steps above until you generate satisfy the termination condition (required)
    if isAcceptable(graph, newClusterOne) == True and isAcceptable(graph, newClusterTwo
                                                                   ) == True and isAllAcceptable(
        graph) == False:  # if acceptable
        threadLock.acquire()
        newScores.append(newDifference)
        edges.append(cutEdge)
        threadLock.release()

    if newDifference < oldDifference: # if improved
        threadLock.acquire()
        newScores.append(newDifference)
        edges.append(cutEdge)
        threadLock.release()


def collectfeasibleEdges(graph, treeNodes, treeEdges, mergedCluster, oldDifference):
    edges = []
    newScores = []
    threads = []

    for i in range(10):  # DIY numbers of threads
        # randomly chose an edge to cut
        cutEdge = random.choice(treeEdges)
        t = threading.Thread(target=getFeasibleEdges,
                             args=(graph, newScores, edges, treeNodes, cutEdge, mergedCluster, oldDifference,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    a = 0
    return edges, newScores


def findEdge(graph, mergedCluster, treeNodes, treeEdges, oldDifference):
    m = 0

    # use case 32. Calculate the acceptability of each newly generated sub-graph (required)
    while (1):
        # use case 33. Generate a feasible set of edges in the spanning tree to cut (required)
        feasibleEdges, newScores = collectfeasibleEdges(graph, treeNodes, treeEdges, mergedCluster, oldDifference)

        if len(feasibleEdges) > 0:
            cutEdge = random.choice(feasibleEdges)
            index = feasibleEdges.index(cutEdge)
            newDifference = newScores[index]

            print("Edge selected to be cut: " + str(cutEdge))
            print("\nnew variation: " + str(newDifference) + ", old variation: " + str(oldDifference))

            return random.choice(feasibleEdges)

        else:
            m += 1
            if (m > 5):
                return None
            continue


def split(graph, mergedCluster, cutEdge, treeNodes):
    # generate new clusters
    newClusterOne, newClusterTwo = getNewClusters(treeNodes, cutEdge, mergedCluster)
    print("new clusters[" + str(newClusterOne.id) + "] and [" + str(newClusterTwo.id) + "] generating...\n")

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
    mergedCluster.updatePop()
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


# Algorithm phase 2
def rebalance(graph, iterationLimit):
    n = 0

    while n < iterationLimit:  # use case 36. Terminate a single districting calculation (required)
        # use case 30. Generate a random districting satisfying constraints (required)
        clusterOne = random.choice(graph.clusters)
        clusterTwo = random.choice(clusterOne.neighbors)
        oldVariation = abs(clusterOne.pop - clusterTwo.pop)  # old score
        print("Selected cluster[" + str(clusterOne.id) + "] and cluster[" + str(clusterTwo.id) + "]")

        # assume to merge the clusters, which means, the merged cluster is "imaginary"
        mergedCluster = merge(clusterOne, clusterTwo)

        # use case 31. Generate a spanning tree of the combined sub-graph above (required)
        print("Generating Spinning Tree...")
        treeNodes, treeEdges = generateTree(mergedCluster)


        print("Spinning Tree: " + str(treeEdges))
        print("Finding an feasible edge...")
        cutEdge = findEdge(graph, mergedCluster, treeNodes, treeEdges, oldVariation)

        if cutEdge == None:
            print("Feasible edge couldn't be found. Leave the original clusters as they were\n")
        else:
            # merge the clusters in real
            combine(clusterOne, clusterTwo, graph)

            # use case 34. Cut the edge in the combined sub-graph (required)
            split(graph, clusterOne, cutEdge, treeNodes)

            graph.printClusters()
            print("--------------------------------------------------------------------------")

            n += 1
