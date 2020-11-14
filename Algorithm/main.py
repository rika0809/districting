import json
from seed import generate_seed
from graph import Graph, Node

if __name__ == '__main__':
    with open('GA_precincts_simplified_plus (1).json') as f:
        data = json.load(f)

    graph = Graph()

    for i in range(len(data['features'])):
        node = Node(data['features'][i]['properties']['ID'], data['features'][i]['properties']['TOTPOP'])
        graph.add_node(node)

    for i in range(len(data['features'])):
        id = data['features'][i]['properties']['ID']
        neighbors_id = data['features'][i]['properties']['Neighbors']

        for neighbor_id in neighbors_id:
            graph.add_edge(id, neighbor_id)

    generate_seed(graph, 14)
    #print("Total population: " + str(graph.totPop()))
    graph.print_clusters()
    print(graph.idealPop())
