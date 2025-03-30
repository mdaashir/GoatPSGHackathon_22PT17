import heapq
import pygame
import json


class NavGraph:
    def __init__(self, json_path):
        with open(json_path, "r") as file:
            data = json.load(file)
            self.vertices = {
                i: (v[0], v[1])
                for i, v in enumerate(data["levels"]["level1"]["vertices"])
            }
            self.edges = {i: [] for i in self.vertices}
            for edge in data["levels"]["level1"]["lanes"]:
                start, end = edge[:2]
                self.edges[start].append(end)

    def get_neighbors(self, node):
        return self.edges.get(node, [])

    def shortest_path(self, start, goal):
        """Implements A* search for shortest path."""
        queue = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while queue:
            _, current = heapq.heappop(queue)

            if current == goal:
                break

            for neighbor in self.get_neighbors(current):
                new_cost = cost_so_far[current] + 1  # Assuming equal weights
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(goal, neighbor)
                    heapq.heappush(queue, (priority, neighbor))
                    came_from[neighbor] = current

        return self.reconstruct_path(came_from, start, goal)

    def heuristic(self, a, b):
        """Euclidean heuristic function."""
        x1, y1 = self.vertices[a]
        x2, y2 = self.vertices[b]
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def reconstruct_path(self, came_from, start, goal):
        """Reconstructs path from came_from dictionary."""
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        path.reverse()
        return path if path[0] == start else []
