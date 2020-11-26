import json
import networkx as nx
import matplotlib.pyplot as plt

from redistricting import rebalance
from seed import generateSeed
from graph import Graph, Node

path = 'GA_precincts_simplified_plus (1).json'

if __name__ == '__main__':
    with open(path) as f:
        data = json.load(f)

    graph = Graph(14, 0.1) # number of districts=14 ,1/2population variation: 0.9ideal~1.1ideal

    for i in range(len(data['features'])):
        node = Node(data['features'][i]['properties']['ID'], data['features'][i]['properties']['TOTPOP'])
        graph.addNode(node)

    for i in range(len(data['features'])):
        id = data['features'][i]['properties']['ID']
        neighborsId = data['features'][i]['properties']['Neighbors']

        for neighborId in neighborsId:
            graph.addEdge(id, neighborId)

    graph.idealPop = int(graph.pop/graph.numCluster)

    print("Generating seed plan...\n")
    generateSeed(graph)

    print("Ideal population: " + str(graph.idealPop))
    print("Population variation: " + str(2 * graph.populationVariation))
    print("Population valid range: " + str(graph.lowerBound) + "-" + str(graph.upperBound))
    print('\n')
    print("Seed plan:")

    graph.printClusters()
    print("\n\nRebalance...\n")
    print("--------------------------------------------------------------------------")
    rebalance(graph, 30)
