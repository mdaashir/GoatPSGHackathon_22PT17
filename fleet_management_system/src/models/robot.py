import uuid
from fleet_management_system.src import LOG_PATH
from fleet_management_system.src.utils.helpers import a_star_search


class Robot:
    def __init__(self, robot_id, start_position, graph):
        self.id = robot_id
        self.current_position = start_position
        self.graph = graph
        self.path = []  # Store path here
        self.status = "waiting"

    def move_to(self, destination):
        path = self.graph.shortest_path(self.current_position, destination)
        if path:
            self.current_position = path[1]  # Move to the next node in the path
        if destination in self.graph.edges[self.current_position]:
            self.current_position = destination
            self.status = "moving"
        else:
            self.status = "waiting"

    def assign_task(self, target_vertex):
        self.path = a_star_search(self.graph, self.current_position, target_vertex)
        if self.path:
            self.status = "moving"

    def move(self, traffic_manager):
        # Move robot based on A* path while avoiding collisions.
        if self.path and self.status == "moving":
            next_pos = self.path[0]

            if traffic_manager.request_move(self, next_pos):
                self.current_position = next_pos
                self.path.pop(0)
                if not self.path:
                    self.status = "idle"
                traffic_manager.release_position(self)
            else:
                self.status = "waiting"
        with open(LOG_PATH / "fleet_logs.txt", "a") as log:
            log.write(f"Robot {self.id} moved to {next_pos}\n")
