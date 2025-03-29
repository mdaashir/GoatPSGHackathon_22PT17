class TrafficManager:
    def __init__(self):
        self.occupied = {}

    def request_move(self, robot, next_position):
        if next_position in self.occupied:
            robot.status = "waiting"
            return False
        self.occupied[robot.id] = next_position
        return True

    def release_position(self, robot):
        if robot.id in self.occupied:
            del self.occupied[robot.id]
