class TrafficManager:
    def __init__(self):
        self.occupied = set()

    def request_move(self, robot, next_position):
        if next_position in self.occupied:
            robot.status = "waiting"
            return False
        self.occupied.add(next_position)
        return True

    def release_position(self, position):
        if position in self.occupied:
            self.occupied.remove(position)
