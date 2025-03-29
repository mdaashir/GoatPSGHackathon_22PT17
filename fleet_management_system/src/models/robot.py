import uuid
from fleet_management_system.src import LOG_PATH
from fleet_management_system.src.utils.helpers import a_star_search


class Robot:
    def __init__(self, start_vertex):
        self.path = None
        self.id = uuid.uuid4().hex[:6]
        self.current_position = start_vertex
        self.target = None
        self.status = "idle"

    def assign_task(self, target_vertex, graph):
        self.path = a_star_search(graph, self.current_position, target_vertex)
        if self.path:
            self.status = "moving"

    def move(self, next_position, traffic_manager):
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
            log.write(f"Robot {self.id} moved to {next_position}\n")
