import json

class NavGraph:
    def __init__(self, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)

        self.vertices = {}
        self.edges = {}

        level_data = data["levels"]["level1"]
        for i, (x, y, meta) in enumerate(level_data["vertices"]):
            self.vertices[i] = (x, y)

        for start, end, meta in level_data["lanes"]:
            speed_limit = meta["speed_limit"]
            self.add_edge(start, end, speed_limit)

    def add_edge(self, u, v, speed_limit):
        # Add bidirectional edge with a speed limit.
        if u not in self.edges:
            self.edges[u] = {}
        if v not in self.edges:
            self.edges[v] = {}

        self.edges[u][v] = speed_limit
        self.edges[v][u] = speed_limit

    def get_neighbors(self, node):
        return list(self.edges.get(node, {}).keys())
