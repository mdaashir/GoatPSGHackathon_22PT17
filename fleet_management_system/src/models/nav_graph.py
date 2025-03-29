import json
import networkx as nx


class NavGraph:
    def __init__(self, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)

        self.graph = nx.Graph()
        self.vertices = {i: tuple(v[:2]) for i, v in enumerate(data["vertices"])}

        for edge in data["lanes"]:
            self.graph.add_edge(edge[0], edge[1])

    def get_neighbors(self, node):
        return list(self.graph.neighbors(node))
