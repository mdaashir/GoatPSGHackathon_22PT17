import logging
from fleet_management_system.src import LOG_PATH


class FleetManager:
    def __init__(self, nav_graph):
        self.nav_graph = nav_graph
        self.robots = {}
        self.setup_logger()

    @staticmethod
    def setup_logger():
        """Sets up logging for robot movements and events."""
        logging.basicConfig(filename= LOG_PATH / "fleet_logs.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def add_robot(self, robot):
        """Registers a new robot."""
        self.robots[robot.robot_id] = robot
        logging.info(f"Robot {robot.robot_id} added at position {robot.current_position}.")

    def register_robot(self, robot):
        """Registers a new robot in the system"""
        self.robots[robot.robot_id] = robot

    def assign_task(self, robot_id, destination):
        """Assigns a task to a robot and handles failure cases"""
        if robot_id not in self.robots:
            robot = self.robots[robot_id]
            old_position = robot.current_position
            robot.move_to(destination)
            logging.info(f"Robot {robot_id} moved from {old_position} to {destination}.")
        else:
            logging.warning(f"Attempted to assign task to unknown Robot ID {robot_id}.")

        robot = self.robots[robot_id]
        robot.assign_task(destination)

        if robot.status == "stuck":
            print(f"Robot {robot_id} is stuck. Reassigning task...")
            alternative_node = self.find_alternative_target(destination)
            if alternative_node:
                robot.assign_task(alternative_node)
            else:
                print(f"No alternative path found for Robot {robot_id}.")

    def find_alternative_target(self, blocked_node):
        """Finds the nearest available node for reassignment"""
        for node in self.nav_graph.vertices:
            if node != blocked_node:
                return node
        return None
