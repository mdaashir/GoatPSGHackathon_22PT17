import heapq


def heuristic(a, b):
    # Calculate Euclidean distance as heuristic.
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def a_star_search(graph, start, goal):
    # Find the shortest path from start to goal using A*.
    queue = []
    heapq.heappush(queue, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while queue:
        _, current = heapq.heappop(queue)

        if current == goal:
            break

        for neighbor in graph.get_neighbors(current):
            new_cost = cost_so_far[current] + heuristic(
                graph.vertices[current], graph.vertices[neighbor]
            )
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(
                    graph.vertices[neighbor], graph.vertices[goal]
                )
                heapq.heappush(queue, (priority, neighbor))
                came_from[neighbor] = current

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from.get(node)
    path.reverse()
    return path
