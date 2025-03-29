import json

class NavGraph:
    def __init__(self, json_path):
        with open(json_path, "r") as file:
            data = json.load(file)

        level_data = data["levels"]["level1"]
        self.vertices = {i: (v[0], v[1]) for i, v in enumerate(level_data["vertices"])}
        self.edges = {i: [] for i in range(len(self.vertices))}

        for edge in level_data["lanes"]:
            start, end, _ = edge
            self.edges[start].append(end)

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
