import json
import networkx as nx


class NavGraph:
    def __init__(self, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)

        self.graph = nx.Graph()
        level_data = data["levels"]["level1"]
        self.vertices = {i: tuple(v[:2]) for i, v in enumerate(level_data["vertices"])}

        for edge in level_data["lanes"]:
            self.graph.add_edge(edge[0], edge[1])

    def get_neighbors(self, node):
        return list(self.graph.neighbors(node))
