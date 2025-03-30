import logging
from fleet_management_system.src.utils.helpers import a_star_search

class Robot:
    def __init__(self, robot_id, start_position, nav_graph):
        self.robot_id = robot_id
        self.current_position = start_position
        self.target_position = None
        self.path = []
        self.nav_graph = nav_graph
        self.status = "waiting"  # ["moving", "waiting", "stuck"]
        self.wait_time = 0  # Counter for detecting deadlocks

    def set_path(self, target):
        """Computes and assigns a path to the target node."""
        self.path = self.nav_graph.shortest_path(self.current_position, target)

    def assign_task(self, destination):
        """Assigns a new destination and computes the shortest path"""
        self.target_position = destination
        self.path = a_star_search(
            self.nav_graph, self.current_position, self.target_position
        )
        if self.path:
            self.status = "moving"
        else:
            self.status = "stuck"

    def move_to(self, target_node):
        """Moves the robot to a new position and logs the movement."""
        if target_node in self.nav_graph.vertices:
            logging.info(f"Robot {self.robot_id} moving from {self.current_position} to {target_node}.")
            self.current_position = target_node
            self.status = "moving"
        else:
            logging.warning(f"Robot {self.robot_id} attempted to move to an invalid node: {target_node}.")
    def move(self, traffic_manager):
        """Moves the robot along its assigned path while handling traffic."""
        if not self.path:
            self.status = "waiting"
            return

        """Moves robot along the path while handling traffic issues"""
        if self.status != "moving" or not self.path:
            return

        next_node = self.path[0]
        if traffic_manager.request_access(self.robot_id, next_node):
            # Move to the next node
            traffic_manager.update_position(self.robot_id, self.current_position, next_node)
            self.current_position = next_node
            self.path.pop(0)
            self.status = "moving"
        else:
            # Path blocked, attempt rerouting
            self.set_path(self.path[-1])  # Recalculate path
            self.status = "stuck" if not self.path else "moving"

        # Release traffic lock after moving
        next_position = self.path[0]

        # Check if the path is blocked
        if traffic_manager.request_move(self.robot_id, next_position):
            # Move robot forward
            self.current_position = next_position
            self.path.pop(0)
            self.wait_time = 0  # Reset wait counter
            if not self.path:
                self.status = "waiting"  # Task completed
        else:
            # Robot is blocked, increase wait time
            self.wait_time += 1

        # If waiting too long, recompute path
        if self.wait_time > 5:
            new_path = a_star_search(
                self.nav_graph, self.current_position, self.target_position
            )
            if new_path:
                self.path = new_path
                self.wait_time = 0  # Reset wait counter
            else:
                self.status = "stuck"

        # Release traffic lock after moving
        traffic_manager.release_position(self.robot_id, self.current_position)
