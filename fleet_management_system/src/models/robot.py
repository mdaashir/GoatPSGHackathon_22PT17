import uuid


class Robot:
    def __init__(self, start_vertex):
        self.id = uuid.uuid4().hex[:6]
        self.current_position = start_vertex
        self.target = None
        self.status = "idle"

    def assign_task(self, target_vertex):
        self.target = target_vertex
        self.status = "moving"

    def move(self, next_position):
        with open("src/logs/fleet_logs.txt", "a") as log:
            log.write(f"Robot {self.id} moved to {next_position}\n")
