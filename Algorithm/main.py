import json
from redistricting import redistricting, printDistricts
from seed import generateSeed
from graph import Graph, Node

iterationLimit = 200

GA = 'GA_precincts_simplified_plus (1).json'
districtsGA = 14

popDifference = 0.1
compactness = 1.5

with open(GA) as f:
    data = json.load(f)

graph = Graph(districtsGA, popDifference, compactness)


def main(graph, data):
    for i in range(len(data['features'])):
        node = Node(data['features'][i]['properties']['ID'], data['features'][i]['properties']['TOTPOP'])
        graph.addNode(node)

    for i in range(len(data['features'])):
        id = data['features'][i]['properties']['ID']
        neighborsId = data['features'][i]['properties']['Neighbors']

        for neighborId in neighborsId:
            graph.addEdge(id, neighborId)

    graph.idealPop = graph.getIdealPop()
    graph.upper = graph.getUpper()
    graph.lower = graph.getLower()

    print("Generating seed plan...\n")
    generateSeed(graph)

    print("Ideal population: " + str(graph.idealPop))
    print("Population variation: " + str(graph.popDifference))
    print("Population valid range: " + str(graph.lower) + "-" + str(graph.upper))
    print('\n')
    print("Seed plan:")
    printDistricts(graph)

    print("\n\nRebalance...\n")
    print("--------------------------------------------------------------------------")
    redistricting(graph, iterationLimit)


if __name__ == '__main__':
    main(graph, data)

