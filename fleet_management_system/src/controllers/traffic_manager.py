class TrafficManager:
    def __init__(self):
        self.occupied_positions = {}
        """Manages traffic flow and prevents collisions."""
        self.occupied_nodes = {}  # {node: robot_id}

    def request_move(self, robot_id, new_position):
        """Checks if the new position is available"""
        if new_position in self.occupied_positions:
            return False
        self.occupied_positions[new_position] = robot_id
        return True

    def release_position(self, robot_id, position):
        """Releases the lock on a position"""
        if (
            position in self.occupied_positions
            and self.occupied_positions[position] == robot_id
        ):
            del self.occupied_positions[position]

    def request_access(self, robot_id, next_node):
        """Checks if a robot can move to the next node safely."""
        if next_node in self.occupied_nodes:
            return False  # Node is occupied, movement not allowed
        return True  # Node is free, movement allowed

    def update_position(self, robot_id, old_node, new_node):
        """Updates the node occupancy when a robot moves."""
        if old_node in self.occupied_nodes:
            del self.occupied_nodes[old_node]
        self.occupied_nodes[new_node] = robot_id