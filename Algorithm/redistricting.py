import random
from graph import Cluster, TreeNode


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
            if neighborId != sourceNodeTwo.id:
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


def isAcceptable(cluster, graph):
    upper = graph.upperBound
    lower = graph.lowerBound
    if upper >= cluster.pop >= lower:
        return True
    else:
        return False


def isAllAcceptable(graph):
    for cluster in graph.clusters:
        if not isAcceptable(cluster, graph):
            return False
    return True


def getNewCluster(id, nodes, mergedCluster):
    newcluster = Cluster()

    newcluster.id = id
    for node in mergedCluster.nodes:
        if node.id in nodes:
            newcluster.nodes.append(node)
    newcluster.updateEdges()
    newcluster.updatePop()

    return newcluster


def updateNeighbors(clusterOne, clusterTwo, mergedCluster, graph):
    for mergedClusterNode in mergedCluster.nodes:
        for neighborNode in mergedClusterNode.neighbors:
            if neighborNode not in clusterOne.nodes and neighborNode not in clusterTwo.nodes:  # it's an external node
                neighborCluster = graph.findCluster(neighborNode)  # find the external cluster the node belongs to

                if mergedClusterNode in clusterOne.nodes:
                    if neighborCluster not in clusterOne.neighbors:
                        clusterOne.neighbors.append(neighborCluster)
                    if clusterOne not in neighborCluster.neighbors:
                        neighborCluster.neighbors.append(clusterOne)

                if mergedClusterNode in clusterTwo.nodes:
                    if neighborCluster not in clusterTwo.neighbors:
                        clusterTwo.neighbors.append(neighborCluster)
                    if clusterTwo not in neighborCluster.neighbors:
                        neighborCluster.neighbors.append(clusterTwo)

    clusterOne.neighbors.append(clusterTwo)
    clusterTwo.neighbors.append(clusterOne)


def findNodesOnCutEdge(treeNodes, cutEdge):
    treeSourceNodeOne = None
    treeSourceNodeTwo = None
    oneId, twoId = cutEdge

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


def findEdge(mergedCluster, graph, treeNodes, treeEdges, oldTotalVariation):
    idealPop = graph.idealPop
    m = 0

    while (1):
        # randomly chose an edge to cut
        cutEdge = random.choice(treeEdges)

        # generate new clusters
        newClusterOne, newClusterTwo = getNewClusters(treeNodes, cutEdge, mergedCluster)

        # calculate new score
        newClusterOneVariation = abs(newClusterOne.pop - idealPop)
        newClusterTwoVariation = abs(newClusterTwo.pop - idealPop)
        newTotalVariation = newClusterOneVariation + newClusterTwoVariation

        if isAcceptable(newClusterOne, graph)==True and isAcceptable(newClusterTwo, graph)==True and isAllAcceptable(graph)==False:
            print("Edge selected to be cut: " + str(cutEdge))
            print("\nnew variation: " + str(newTotalVariation) + ", old variation: " + str(oldTotalVariation))
            print("new clusters[" + str(newClusterOne.id) + "] and [" + str(newClusterTwo.id) + "] generating...\n")
            return cutEdge
        elif newTotalVariation < oldTotalVariation:
            print("Edge selected to be cut: " + str(cutEdge))
            print("\nnew variation: " + str(newTotalVariation) + ", old variation: " + str(oldTotalVariation))
            print("new clusters[" + str(newClusterOne.id) + "] and [" + str(newClusterTwo.id) + "] generating...\n")
            return cutEdge
        else:
            m += 1
            if (m > 500):
                return None
            continue


def split(cutEdge, treeNodes, mergedCluster, graph):
    # generate new clusters
    newClusterOne, newClusterTwo = getNewClusters(treeNodes, cutEdge, mergedCluster)

    # update new clusters' and surrounded cluster's neighbors
    updateNeighbors(newClusterOne, newClusterTwo, mergedCluster, graph)

    # erase the merged cluster from the graph
    for cluster in graph.clusters:
        if mergedCluster in cluster.neighbors:
            cluster.removeNeighbor(mergedCluster)
    graph.removeCluster(mergedCluster)

    # add new clusters on graph
    graph.clusters.append(newClusterOne)
    graph.clusters.append(newClusterTwo)


def merge(cluster, target, graph):
    mergedCluster = Cluster()

    mergedCluster.nodes = cluster.nodes + target.nodes

    mergedCluster.updatePop()
    mergedCluster.updateEdges()

    for clu in target.neighbors:
        if cluster == clu:
            clu.removeNeighbor(target)
            continue
        if cluster not in clu.neighbors:
            clu.addNeighbor(cluster)
        if clu not in cluster.neighbors:
            cluster.addNeighbor(clu)
        clu.removeNeighbor(target)

    # for clu in graph.clusters:
    #    if target in clu.neighbors:
    #        clu.removeNeighbor(target)

    graph.removeCluster(target)


def rebalance(graph, iterationLimit):
    n = 0
    idealPop = graph.idealPop

    while n < iterationLimit:
        clusterOne = random.choice(graph.clusters)
        clusterTwo = random.choice(clusterOne.neighbors)
        print("Selected cluster[" + str(clusterOne.id) + "] and cluster[" + str(clusterTwo.id) + "]")

        clusterOneVariation = abs(clusterOne.pop - idealPop)
        clusterTwoVariation = abs(clusterTwo.pop - idealPop)
        totalVariation = clusterOneVariation + clusterTwoVariation

        print("Merging...")
        merge(clusterOne, clusterTwo, graph)

        print("Generating Spinning Tree...")
        treeNodes, treeEdges = generateTree(clusterOne)

        print("Spinning Tree: " + str(treeEdges))
        print("Finding an feasible edge...")
        cutEdge = findEdge(clusterOne, graph, treeNodes, treeEdges, totalVariation)

        if cutEdge == None:
            print("Feasible edge couldn't be found after 500 iterations. Leave the original clusters as they were")
        else:
            split(cutEdge, treeNodes, clusterOne, graph)
            graph.printClusters()
            print("--------------------------------------------------------------------------")
            n += 1

        a = 0

