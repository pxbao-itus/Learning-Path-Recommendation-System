import igraph

graph = igraph.Graph(directed=True)

graph.add_vertices(9)
graph.vs["id"] = [4037, 910, 1458, 1875, 724, 23434, 56456, 3423, 23423]

graph.add_edges([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8)])

layout = graph.layout_kamada_kawai()
layout = graph.layout("kk")
igraph.plot(graph, layout=layout)
