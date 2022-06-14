import os
from pathlib import Path

import igraph

def visualize_learning_path(set_course, index):
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
#
# vxs = [
#     "Visualization for Data Journalism",
#     "Share Data Through the Art of Visualization",
#     "Exploring ?and ?Preparing ?your ?Data with BigQuery",
#     "The Fundamentals of Business Intelligence (BI)",
#     "BigQuery Basics for Data Analysts",
#     "Learn JIRA for Beginners",
#     "Apache Spark: Hands-on Specialization for Big Data Analytics",
#     "Learn Microsoft Power BI for Data Science",
#     "Data Analysis with Pandas: 3-in-1",
# ]
# visualize_learning_path(vxs, 1)
