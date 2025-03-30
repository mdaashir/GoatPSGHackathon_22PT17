import pygame
import logging
from fleet_management_system.src import LOG_PATH
from fleet_management_system.src.controllers.fleet_manager import FleetManager
from fleet_management_system.src.controllers.traffic_manager import TrafficManager
from fleet_management_system.src.models.nav_graph import NavGraph
from fleet_management_system.src.models.robot import Robot

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)


class FleetGUI:
    def __init__(self, json_path):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fleet Management System")
        self.graph = NavGraph(json_path)
        self.fleet_manager = FleetManager(self.graph)
        self.traffic_manager = TrafficManager()

        self.robots = [
            Robot(i, start_node, self.graph)
            for i, start_node in list(enumerate(self.graph.vertices.keys()))[:3]
        ]

        for robot in self.robots:
            self.fleet_manager.register_robot(robot)

        self.selected_robot = None
        self.running = True  # Pause/Resume Control
        self.robot_counter = 1  # Unique ID counter for new robots

    def draw_graph(self):
        """Draws the navigation graph"""
        for start, neighbors in self.graph.edges.items():
            x1, y1 = self.graph.vertices[start]
            for end in neighbors:
                x2, y2 = self.graph.vertices[end]
                pygame.draw.line(
                    self.screen,
                    BLACK,
                    (x1 * 50, -y1 * 50 + 500),
                    (x2 * 50, -y2 * 50 + 500),
                    2,
                )

        for node, (x, y) in self.graph.vertices.items():
            pygame.draw.circle(self.screen, GREEN, (x * 50, -y * 50 + 500), 8)

    def draw_robots(self):
        """Draws robots on the screen"""
        for robot in self.robots:
            x, y = self.graph.vertices[robot.current_position]
            color = (
                RED
                if robot.status == "stuck"
                else YELLOW if robot.status == "waiting" else GREEN
            )
            pygame.draw.circle(self.screen, color, (x * 50, -y * 50 + 500), 10)

            # Draw robot ID for tracking
            font = pygame.font.Font(None, 24)
            text = font.render(f"R{robot.robot_id}", True, BLUE)
            self.screen.blit(text, (x * 50 - 5, -y * 50 + 490))

    def draw_status(self):
        """Displays the status of all robots"""
        font = pygame.font.Font(None, 24)
        y_offset = 10
        for robot in self.robots:
            status_text = f"Robot {robot.robot_id}: {robot.status}"
            text = font.render(status_text, True, BLACK)
            self.screen.blit(text, (10, y_offset))
            y_offset += 20

    def get_closest_node(self, x, y):
        """Finds the closest graph node to the clicked position."""
        return min(self.graph.vertices, key=lambda v: (self.graph.vertices[v][0] * 50 - x) ** 2 + (self.graph.vertices[v][1] * 50 - y) ** 2)

    def draw_logs(self):
        """Displays logs dynamically in the GUI."""
        font = pygame.font.Font(None, 20)
        y_offset = 10
        try:
            with open(LOG_PATH / "fleet_logs.txt", "r") as log_file:
                lines = log_file.readlines()[-5:]  # Show last 5 log entries
                for line in lines:
                    text_surface = font.render(line.strip(), True, (0, 0, 0))
                    self.screen.blit(text_surface, (10, y_offset))
                    y_offset += 20
        except FileNotFoundError:
            pass

    def run(self):
        """Main loop for GUI interaction"""
        running = True
        clock = pygame.time.Clock()

        while running:
            self.screen.fill(WHITE)
            self.draw_graph()
            self.draw_robots()
            self.draw_status()
            self.draw_logs()
            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    closest_node = self.get_closest_node(x, y)

                    if self.selected_robot is None:
                        # Select Robot
                        new_robot = Robot(self.robot_counter, closest_node, self.graph)
                        self.robots.append(new_robot)
                        self.fleet_manager.add_robot(new_robot)
                        self.robot_counter += 1
                        for robot in self.robots:
                            if robot.current_position == closest_node:
                                self.selected_robot = robot
                                break
                    else:
                        # Assign Task
                        self.fleet_manager.assign_task(
                            self.selected_robot.robot_id, closest_node
                        )
                        self.selected_robot = None

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Pause/Resume system
                        self.running = not self.running

            # Move robots only if running
            if self.running:
                for robot in self.robots:
                    robot.move(self.traffic_manager)

        pygame.quit()
