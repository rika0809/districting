import json
import cProfile, pstats
from redistricting import redistricting, printDistricts
from seed import generateSeed
from graph import Graph, Node


iterationLimit = 50

GA = 'GA.json'
districtsGA = 14

MI = 'MI.json'
districtsMI = 4

LA = 'LA.json'
districtsLA = 6

popDifference = 0.03
compactness = 0.1

with open(GA) as f:
    data = json.load(f)

graph = Graph(districtsGA, popDifference, compactness)

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


def generatePlan():
    generateSeed(graph)
    redistricting(graph, iterationLimit)


if __name__ == '__main__':
    #profiler = cProfile.Profile()
    #profiler.enable()

    generatePlan()

    #profiler.enable()
    #state = pstats.Stats(profiler)
    #state.dump_stats('profile.out')

