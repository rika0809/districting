import random
from seed import merge
from graph import Cluster, TreeNode


def generateTree(cluster):
    treeNodes = []
    treeEdges = []

    s = random.choice(range(len(cluster.nodes)))

    for node in cluster.nodes:
        treeNodes.append(TreeNode(node.id))

    visited = [False] * len(cluster.nodes)
    queue = []
    queue.append(cluster.nodes[s])
    visited[s] = True

    while len(queue) > 0:
        sourceNode = queue.pop(0)
        uid = sourceNode.id
        # print("node" + str(u_id))
        for neighbor in sourceNode.neighbors:
            if neighbor in cluster.nodes:
                s = cluster.nodes.index(neighbor)
                if not visited[s]:
                    vid = neighbor.id
                    treeEdges.append((uid, vid))
                    visited[s] = True
                    queue.append(cluster.nodes[s])

                    for treeNode in treeNodes:
                        if treeNode.id == uid:
                            treeNode.addNeighbor(vid)
                        if treeNode.id == vid:
                            treeNode.addNeighbor(uid)

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
    if upper >= cluster.pop >= lower: #and len(cluster.edge_cut) < graph.edgeCut
        return True
    else:
        return False


def findEdge(cluster, graph, treeNodes, treeEdges, oldTotalVariation):
    idealPop = graph.idealPop
    m = 0
    while (1):
        cutEdge = random.choice(treeEdges)

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

        nodesOne = getClusterNodes(treeNodes, treeSourceNodeOne, treeSourceNodeTwo)
        nodesTwo = getClusterNodes(treeNodes, treeSourceNodeTwo, treeSourceNodeOne)

        newclusterOne = Cluster()
        newclusterOne.id = treeSourceNodeOne.id
        for node in cluster.nodes:
            if node.id in nodesOne:
                newclusterOne.nodes.append(node)
        newclusterOne.updateEdges()
        newclusterOne.updatePop()

        newclusterTwo = Cluster()
        newclusterTwo.id = treeSourceNodeTwo.id
        for node in cluster.nodes:
            if node.id in nodesTwo:
                newclusterTwo.nodes.append(node)
        newclusterTwo.updateEdges()
        newclusterTwo.updatePop()

        newClusterOneVariation = abs(newclusterOne.pop - idealPop)
        newClusterTwoVariation = abs(newclusterTwo.pop - idealPop)
        newTotalVariation = newClusterOneVariation + newClusterTwoVariation
        newEdgeCutOne = len(newclusterOne.edgeCut)
        newEdgeCutTwo = len(newclusterTwo.edgeCut)
        newTotalCutEdge = newEdgeCutOne + newEdgeCutTwo

        if isAcceptable(newclusterOne, graph) == True and isAcceptable(newclusterTwo, graph) == True:
            print("Edge selected to be cut" + str(cutEdge))
            print("\nnew variation: " + str(newTotalVariation) + ", old variation: " + str(oldTotalVariation))
            print("new clusters[" + str(newclusterOne.id) + "] and [" + str(newclusterTwo.id) + "] generating...\n")
            return cutEdge
        elif newTotalVariation <= oldTotalVariation:
            print("Edge selected to be cut" + str(cutEdge))
            print("\nnew variation: " + str(newTotalVariation) + ", old variation: " + str(oldTotalVariation))
            print("new clusters[" + str(newclusterOne.id) + "] and [" + str(newclusterTwo.id) + "] generating...\n")
            return cutEdge
        else:
            m += 1
            if (m > 500):
                print("Feasible edges couldn't be found")
                return None
            continue


def split(cutEdge, treeNodes, cluster, graph):
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

    nodesOne = getClusterNodes(treeNodes, treeSourceNodeOne, treeSourceNodeTwo)
    nodesTwo = getClusterNodes(treeNodes, treeSourceNodeTwo, treeSourceNodeOne)

    newclusterOne = Cluster()
    newclusterOne.id = treeSourceNodeOne.id
    for node in cluster.nodes:
        if node.id in nodesOne:
            newclusterOne.nodes.append(node)
    newclusterOne.updateEdges()
    newclusterOne.updatePop()

    newclusterTwo = Cluster()
    newclusterTwo.id = treeSourceNodeTwo.id
    for node in cluster.nodes:
        if node.id in nodesTwo:
            newclusterTwo.nodes.append(node)
    newclusterTwo.updateEdges()
    newclusterTwo.updatePop()


    for node in newclusterOne.nodes:
        for neighborNode in node.neighbors:
            if neighborNode not in newclusterTwo.nodes:
                neighborCluster = graph.findCluster(neighborNode)
                if neighborCluster not in newclusterOne.neighbors and neighborCluster in cluster.neighbors:
                    newclusterOne.neighbors.append(neighborCluster)

    for node in newclusterTwo.nodes:
        for neighborNode in node.neighbors:
            if neighborNode not in newclusterOne.nodes:
                neighborCluster = graph.findCluster(neighborNode)
                if neighborCluster not in newclusterTwo.neighbors and neighborCluster in cluster.neighbors:
                    newclusterTwo.neighbors.append(neighborCluster)

    newclusterOne.neighbors.append(newclusterTwo)
    newclusterTwo.neighbors.append(newclusterOne)

    for clu in graph.clusters:
        if cluster in clu.neighbors:
            clu.removeNeighbor(cluster)

    graph.removeCluster(cluster)

    for neighborCluster in cluster.neighbors:
        for uid, vid in neighborCluster.edgeCut:
            v = graph.findNode(vid)
            if v in newclusterOne.nodes and newclusterOne not in neighborCluster.neighbors:
                neighborCluster.neighbors.append(newclusterOne)
            if v in newclusterTwo.nodes and newclusterTwo not in neighborCluster.neighbors:
                neighborCluster.neighbors.append(newclusterTwo)

    graph.clusters.append(newclusterOne)
    graph.clusters.append(newclusterTwo)


def rebalance(graph):
    n = 0
    idealPop = graph.idealPop
    while (n < 2):
        clusterOne = random.choice(graph.clusters)
        clusterTwo = random.choice(clusterOne.neighbors)
        print("Selected cluster[" + str(clusterOne.id) + "] and cluster[" + str(clusterTwo.id) +"]")

        clusterOneVariation = abs(clusterOne.pop - idealPop)
        clusterTwoVariation = abs(clusterTwo.pop - idealPop)
        totalVariation = clusterOneVariation + clusterTwoVariation
        oldEdgeCutOne = len(clusterOne.edgeCut)
        oldEdgeCutTwo = len(clusterTwo.edgeCut)
        totalCutEdge = oldEdgeCutOne + oldEdgeCutTwo

        print("Merging...")
        merge(clusterOne, clusterTwo, graph)
        print("Generating Spinning Tree...")
        treeNodes, treeEdges = generateTree(clusterOne)
        print("Spinning Tree: " + str(treeEdges))
        print("Finding an feasible edge...")
        cutEdge = findEdge(clusterOne, graph, treeNodes, treeEdges, totalVariation)
        if cutEdge == None:
            print("Algorithm exit....")
            return

        split(cutEdge, treeNodes, clusterOne, graph)

        graph.printClusters()
        print("--------------------------------------------------------------------------")

        n += 1

