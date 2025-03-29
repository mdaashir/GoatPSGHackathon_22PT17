import pygame
from fleet_management_system.src import DATA_PATH
from fleet_management_system.src.models.nav_graph import NavGraph
from fleet_management_system.src.models.robot import Robot

WIDTH, HEIGHT = 800, 600
WHITE, BLUE, RED, GREEN = (255, 255, 255), (0, 0, 255), (255, 0, 0), (0, 255, 0)


class FleetGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.graph = NavGraph(DATA_PATH / "nav_graph_1.json")
        self.robots = []

    def draw_graph(self):
        self.screen.fill(WHITE)
        for v1, v2 in self.graph.graph.edges:
            pygame.draw.line(
                self.screen, BLUE, self.graph.vertices[v1], self.graph.vertices[v2], 2
            )

        for v in self.graph.vertices:
            pygame.draw.circle(self.screen, GREEN, self.graph.vertices[v], 5)

    def draw_robots(self):
        for robot in self.robots:
            color = RED if robot.status == "waiting" else GREEN
            pygame.draw.circle(self.screen, color, self.graph.vertices[robot.current_position], 10)

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            self.screen.fill(WHITE)
            self.draw_graph()
            self.draw_robots()

            pygame.display.flip()
            clock.tick(30)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for v, pos in self.graph.vertices.items():
                        if abs(pos[0] - x) < 10 and abs(pos[1] - y) < 10:
                            self.robots.append(Robot(v))

        pygame.quit()
