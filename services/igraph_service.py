import os
from pathlib import Path

import igraph


def visualize_learning_path_v1(set_course, index):
    i_graph = igraph.Graph(directed=True)
    i_graph.add_vertices(set_course.__len__())
    i_graph.vs["name"] = set_course
    edges = []
    for i in range(set_course.__len__() - 1):
        edges.append((i, i + 1))
    i_graph.add_edges(edges)
    layout = i_graph.layout_circle()
    visual_style = {"vertex_size": 100, "layout": layout, "vertex_color": "cyan", "vertex_label": i_graph.vs["name"],
                    "edge_width": 5, "bbox": (900, 900), "margin": 100}
    file_name = f"static/learning-path-{index}.png"
    print(file_name)
    igraph.plot(i_graph, file_name, **visual_style)


def visualize_learning_path_v2(path_final, index):
    i_graph = igraph.Graph(directed=True)
    counter = 0
    size_graph = 0
    for path in path_final:
        size_graph = size_graph + path.__len__()
    i_graph.add_vertices(size_graph)
    edges = []
    vertexs = []
    for path in path_final:
        vertexs.extend(path)
        if path.__len__() > 0:
            for i in range(path.__len__() - 1):
                edges.append((counter + i, counter + i + 1))
            counter = counter + path.__len__()
        else:
            counter = counter + 1
    i_graph.vs["id"] = vertexs
    i_graph.add_edges(edges)
    max_size = 0
    for sub_path in path_final:
        if max_size < sub_path.__len__():
            max_size = sub_path.__len__()
    layout = i_graph.layout_reingold_tilford()
    visual_style = {"vertex_size": 50, "layout": layout, "vertex_color": "orange", "vertex_label": i_graph.vs["id"],
                    "edge_width": 2, "bbox": (path_final.__len__() * 50 + 100, max_size * 70 + 100), "margin": 50}
    file_name = f"static/learning-path-{index}.png"
    igraph.plot(i_graph, file_name, **visual_style)


# visualize_learning_path_v2([[244], [287, 262], [282, 272, 311, 302, 316, 323], [335, 340, 361, 350, 427, 403]], 1)
